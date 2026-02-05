const state = {
    pageType: document.body?.dataset?.page || '',
    category: null,
    allEntries: [],
    visibleCount: 8
};

const PAGE_SIZE = 8;

document.addEventListener('DOMContentLoaded', () => {
    initUI();
});

function initUI() {
    if (state.pageType === 'daily') {
        state.visibleCount = 5;
    }
    setupLoadMore();
    loadAppData();
}

async function loadAppData() {
    const pageType = state.pageType;

    // About Me and Index don't need to fetch JSON
    if (pageType === 'about' || pageType === 'index') return;

    const container = document.getElementById('content-wrap');
    const loadStart = performance.now();
    showLoading(container);

    try {
        const res = await fetch('updates.json');
        if (!res.ok) throw new Error('JSON missing');
        const data = await res.json();
        state.allEntries = normalizeEntries(data);
        await ensureMinLoadTime(loadStart);

        if (pageType === 'dashboard') {
            updatePageTitle('Dashboard');
            renderUpdates();
        } else if (pageType === 'fields') {
            updatePageTitle('Fields');
            renderCategories();
        } else if (pageType === 'category') {
            renderCategorySpecific();
        } else if (pageType === 'daily') {
            renderDaily();
        }
    } catch (err) {
        console.error('Data Error:', err);
        if (container) {
            container.innerHTML = `<p style="text-align:center; padding:100px 0; opacity:0.5;">Logs currently unavailable.</p>`;
        }
    }
}

function normalizeEntries(entries) {
    if (!Array.isArray(entries)) return [];
    return entries
        .filter(entry => entry && entry.date)
        .sort((a, b) => new Date(b.date) - new Date(a.date));
}

function showLoading(container) {
    if (!container) return;
    container.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>Loading...</p>
        </div>
    `;
}

function ensureMinLoadTime(startTime) {
    const elapsed = performance.now() - startTime;
    if (elapsed < 5) return Promise.resolve();
    if (elapsed >= 500) return Promise.resolve();
    const waitMs = Math.max(500 - elapsed, 0);
    return new Promise(resolve => setTimeout(resolve, waitMs));
}

function setupLoadMore() {
    const btn = document.getElementById('load-more-btn');
    if (!btn) return;
    btn.addEventListener('click', () => {
        state.visibleCount += PAGE_SIZE;
        renderCurrentPage();
    });
}

function renderCurrentPage() {
    if (state.pageType === 'dashboard') {
        renderUpdates();
    } else if (state.pageType === 'category') {
        renderCategorySpecific();
    } else if (state.pageType === 'daily') {
        renderDaily();
    }
}

function updatePageTitle(text) {
    const titleEl = document.getElementById('page-title-text') || document.querySelector('.page_title');
    if (titleEl) titleEl.innerText = text;
    document.title = `${text} - Log`;
}

function renderUpdates() {
    const container = document.getElementById('content-wrap');
    if (!container) return;

    const entries = state.allEntries.slice(0, state.visibleCount);
    container.innerHTML = buildUpdatesHTML(entries);
    updateLoadMore(entries.length, state.allEntries.length);
}

function renderCategories() {
    const container = document.getElementById('content-wrap');
    if (!container) return;

    const categories = Array.from(
        new Set(state.allEntries.map(entry => entry.cat).filter(Boolean))
    ).sort((a, b) => a.localeCompare(b));

    if (!categories.length) {
        container.innerHTML = `<p style="text-align:center; padding:60px 0; opacity:0.5;">No categories yet.</p>`;
        return;
    }

    const listHTML = categories
        .map(cat => `<div class="cat_link"><a href="Category.html?cat=${encodeURIComponent(cat)}">${cat}</a></div>`)
        .join('');

    container.innerHTML = `<div class="cat_list">${listHTML}</div>`;
}

function renderCategorySpecific() {
    const container = document.getElementById('content-wrap');
    if (!container) return;

    const category = getCategoryFromUrl() || getStoredCategory();
    if (!category) {
        container.innerHTML = `<p style="text-align:center; padding:60px 0; opacity:0.5;">Select a category from Fields.</p>`;
        updateLoadMore(0, 0);
        return;
    }

    state.category = category;
    storeCategory(category);
    updatePageTitle(category);

    const filtered = state.allEntries.filter(entry => entry.cat === category);
    if (!filtered.length) {
        container.innerHTML = `<p style="text-align:center; padding:60px 0; opacity:0.5;">No entries for ${category} yet.</p>`;
        updateLoadMore(0, 0);
        return;
    }

    const visible = filtered.slice(0, state.visibleCount);
    container.innerHTML = buildUpdatesHTML(visible);
    updateLoadMore(visible.length, filtered.length);
}

function renderDaily() {
    const todayEntry = getTodayEntry(state.allEntries);

    const dateEl = document.getElementById('today-date');
    const workEl = document.getElementById('today-work');
    const streakEl = document.getElementById('today-streak-count');
    const historyEl = document.getElementById('daily-history');

    const todayDate = new Date();
    if (dateEl) {
        dateEl.innerText = todayDate.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    if (workEl) {
        workEl.innerHTML = todayEntry?.desc || `<span class="muted">No log yet.</span>`;
    }

    if (streakEl) {
        streakEl.innerText = String(calculateStreak(state.allEntries));
    }

    if (historyEl) {
        const historyData = buildDailyHistory(state.allEntries, state.visibleCount);
        historyEl.innerHTML = historyData.html;
        updateLoadMore(historyData.visibleCount, historyData.totalCount);
    }
}

function buildUpdatesHTML(entries) {
    if (!entries.length) {
        return `<p style="text-align:center; padding:60px 0; opacity:0.5;">No entries yet.</p>`;
    }

    const groups = groupByDate(entries);

    return groups
        .map(group => {
            const dateParts = formatDateParts(group.date);
            const itemsHTML = group.items.map(renderUpdateItem).join('');

            return `
                <div class="ud_info">
                    <div class="ud_left">
                        <div class="ud_date">${dateParts.day}</div>
                        <div class="ud_monthyear">${dateParts.monthYear}</div>
                    </div>
                    <div class="ud_right">
                        ${itemsHTML}
                    </div>
                </div>
            `;
        })
        .join('');
}

function renderUpdateItem(entry) {
    const title = entry.title || '';
    const desc = entry.desc || '';
    const cat = entry.cat || '';

    return `
        <div class="ud_text">
            <div class="ud_header">
                <p class="ud_cat">${cat}</p>
                <p class="ud_title">${title}</p>
            </div>
            <div class="ud_description">
                <p>${desc}</p>
            </div>
        </div>
    `;
}

function groupByDate(entries) {
    const groups = [];
    let current = null;

    entries.forEach(entry => {
        if (!current || current.date !== entry.date) {
            current = { date: entry.date, items: [] };
            groups.push(current);
        }
        current.items.push(entry);
    });

    return groups;
}

function formatDateParts(dateStr) {
    const dateObj = new Date(dateStr);
    if (Number.isNaN(dateObj.getTime())) {
        return { day: '', monthYear: dateStr || '' };
    }

    return {
        day: String(dateObj.getDate()).padStart(2, '0'),
        monthYear: dateObj.toLocaleDateString('en-US', {
            month: 'short',
            year: 'numeric'
        })
    };
}

function getTodayKey() {
    return formatDateKey(new Date());
}

function getTodayEntry(entries) {
    const todayKey = getTodayKey();
    return entries.find(entry => entry.date === todayKey) || null;
}

function calculateStreak(entries) {
    if (!entries.length) return 0;
    const dateSet = new Set(entries.map(entry => entry.date));
    let count = 0;
    const current = new Date();

    while (true) {
        const key = formatDateKey(current);
        if (!dateSet.has(key)) break;
        count += 1;
        current.setDate(current.getDate() - 1);
    }

    return count;
}

function buildDailyHistory(entries, limit) {
    const todayKey = getTodayKey();
    const historyEntries = entries.filter(entry => entry.date !== todayKey);
    const groups = groupByDate(historyEntries);
    const visibleGroups = groups.slice(0, limit);

    if (!groups.length) {
        return {
            html: `<div class="daily-history-empty">No previous logs yet.</div>`,
            visibleCount: 0,
            totalCount: 0
        };
    }

    const html = visibleGroups
        .map(group => {
            const dateLabel = formatFullDate(group.date);
            const itemsHtml = group.items
                .map(item => {
                    return `
                        <div class="daily-history-item">
                            <div class="daily-history-cat">${item.cat || ''}</div>
                            <div class="daily-history-item-title">${item.title || ''}</div>
                            <div class="daily-history-desc">${item.desc || ''}</div>
                        </div>
                    `;
                })
                .join('');

            return `
                <div class="daily-history-card">
                    <div class="daily-history-date">${dateLabel}</div>
                    ${itemsHtml}
                </div>
            `;
        })
        .join('');

    return {
        html,
        visibleCount: visibleGroups.length,
        totalCount: groups.length
    };
}

function formatFullDate(dateStr) {
    const dateObj = new Date(dateStr);
    if (Number.isNaN(dateObj.getTime())) return dateStr || '';
    return dateObj.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

function formatDateKey(dateObj) {
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}


function updateLoadMore(visibleCount, totalCount) {
    const btn = document.getElementById('load-more-btn');
    if (!btn) return;

    if (visibleCount < totalCount) {
        btn.style.display = 'inline-block';
    } else {
        btn.style.display = 'none';
    }
}

function getCategoryFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('cat') || params.get('category') || '';
}

function storeCategory(category) {
    try {
        localStorage.setItem('selectedCategory', category);
    } catch (err) {
        console.warn('Unable to store category', err);
    }
}

function getStoredCategory() {
    try {
        return localStorage.getItem('selectedCategory') || '';
    } catch (err) {
        return '';
    }
}

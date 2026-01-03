// Header Scroll Effect
const header = document.querySelector('.header');
const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
const navList = document.querySelector('.nav-list');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Dynamic Menu Logic
function setupDynamicMenu() {
    const navList = document.querySelector('.nav-list');
    if (!navList) return;

    // If menu is already rendered with a server-side dropdown, don't re-process
    if (navList.querySelector('.dropdown-wrapper')) return;

    // Only run on desktop
    if (window.innerWidth <= 768) return;

    // Check if already processed
    if (navList.dataset.processed === 'true') return;

    const items = Array.from(navList.children);
    const maxItems = 5;

    if (items.length > maxItems) {
        const visibleItems = items.slice(0, maxItems);
        const hiddenItems = items.slice(maxItems);

        // Clear list
        navList.innerHTML = '';

        // Add visible items back
        visibleItems.forEach(item => navList.appendChild(item));

        // Create dropdown
        const dropdownLi = document.createElement('li');
        dropdownLi.className = 'dropdown-wrapper';

        dropdownLi.innerHTML = `
            <div class="dropdown-trigger">
                Еще
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 9l6 6 6-6"/>
                </svg>
            </div>
            <ul class="dropdown-menu"></ul>
        `;

        const dropdownMenu = dropdownLi.querySelector('.dropdown-menu');

        hiddenItems.forEach(item => {
            dropdownMenu.appendChild(item);
        });

        navList.appendChild(dropdownLi);

        // Click functionality only (no hover)
        const trigger = dropdownLi.querySelector('.dropdown-trigger');
        trigger.addEventListener('click', (e) => {
            e.stopPropagation();
            dropdownMenu.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!dropdownLi.contains(e.target)) {
                dropdownMenu.classList.remove('active');
            }
        });

        // Mark as processed
        navList.dataset.processed = 'true';
    }
}

// Run on load
document.addEventListener('DOMContentLoaded', () => {
    setupDynamicMenu();
});

// Mobile Menu Toggle
if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenuBtn.classList.toggle('active');
        navList.classList.toggle('active');
    });
}

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (!header.contains(e.target) && navList && navList.classList.contains('active')) {
        navList.classList.remove('active');
        if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
    }
});

// Accordion (for service.html)
const accItems = document.querySelectorAll('.accordion-item');

accItems.forEach(item => {
    const headerEl = item.querySelector('.accordion-header');

    if (headerEl) {
        headerEl.addEventListener('click', () => {
            const content = item.querySelector('.accordion-content');
            const icon = item.querySelector('.accordion-icon');

            // Toggle current item
            // Check if already active
            const isActive = content.classList.contains('active');

            // Close all items
            document.querySelectorAll('.accordion-content').forEach(c => c.classList.remove('active'));
            document.querySelectorAll('.accordion-icon').forEach(i => i.style.transform = 'rotate(0deg)');

            if (!isActive) {
                content.classList.add('active');
                if (icon) icon.style.transform = 'rotate(180deg)';
            }
        });
    }
});

// 360 Modal (Placeholder functionality)
function open360Modal() {
    const modal = document.getElementById('modal-360');
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
    }
}

function close360Modal() {
    const modal = document.getElementById('modal-360');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Close modal on outside click
const modal = document.getElementById('modal-360');
if (modal) {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            close360Modal();
        }
    });
}

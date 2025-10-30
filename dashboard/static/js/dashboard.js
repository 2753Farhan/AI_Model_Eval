// Dashboard JavaScript for CodeQualBench

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    // Auto-highlight all code blocks
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }

    // Add loading states to charts
    const chartContainers = document.querySelectorAll('[id$="Chart"]');
    chartContainers.forEach(container => {
        container.innerHTML = '<div class="text-center text-muted py-4"><i class="fas fa-spinner fa-spin me-2"></i>Loading chart...</div>';
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            filterProblems(searchTerm);
        }, 300));
    }

    // Add tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add copy to clipboard functionality for code blocks
    document.querySelectorAll('pre code').forEach(codeBlock => {
        const pre = codeBlock.parentElement;
        if (pre && !pre.querySelector('.copy-btn')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn btn-sm btn-outline-secondary copy-btn';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.style.position = 'absolute';
            copyBtn.style.top = '10px';
            copyBtn.style.right = '10px';
            copyBtn.style.opacity = '0.7';
            copyBtn.title = 'Copy to clipboard';
            
            copyBtn.addEventListener('click', function() {
                copyToClipboard(codeBlock.textContent);
                this.innerHTML = '<i class="fas fa-check"></i>';
                this.classList.remove('btn-outline-secondary');
                this.classList.add('btn-success');
                
                setTimeout(() => {
                    this.innerHTML = '<i class="fas fa-copy"></i>';
                    this.classList.remove('btn-success');
                    this.classList.add('btn-outline-secondary');
                }, 2000);
            });
            
            pre.style.position = 'relative';
            pre.appendChild(copyBtn);
        }
    });
}

// Utility function to filter problems
function filterProblems(searchTerm) {
    const rows = document.querySelectorAll('#problemsTable tbody tr');
    let visibleCount = 0;
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const isVisible = text.includes(searchTerm);
        row.style.display = isVisible ? '' : 'none';
        
        if (isVisible) {
            visibleCount++;
            row.classList.add('highlight');
            setTimeout(() => row.classList.remove('highlight'), 1000);
        }
    });
    
    // Update table header with result count
    const tableHeader = document.querySelector('#problemsTable thead th:first-child');
    if (tableHeader) {
        const originalText = 'Problem ID';
        if (searchTerm) {
            tableHeader.textContent = `${originalText} (${visibleCount} results)`;
        } else {
            tableHeader.textContent = originalText;
        }
    }
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Copy to clipboard utility
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

// Export data functionality
function exportToCSV() {
    // This would need to be implemented with server-side support
    alert('Export feature would download the current data as CSV');
}

// Quality assessment helper
function calculateQualityScore(problem) {
    if (!problem.maintainability_index || !problem.cyclomatic_complexity) {
        return null;
    }
    
    const maintainabilityScore = (problem.maintainability_index / 100) * 60;
    const complexityScore = Math.max(0, (10 - problem.cyclomatic_complexity) * 4);
    const totalScore = maintainabilityScore + complexityScore;
    
    return Math.min(100, Math.max(0, totalScore));
}

// Chart error handling
function handleChartError(chartId, error) {
    const container = document.getElementById(chartId);
    if (container) {
        container.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="fas fa-exclamation-triangle fa-2x mb-2"></i>
                <p>Failed to load chart</p>
                <small>${error.message || 'Unknown error'}</small>
            </div>
        `;
    }
}

// Add some visual feedback for interactions
document.addEventListener('click', function(e) {
    if (e.target.matches('.btn, .card, .problem-row')) {
        e.target.style.transform = 'scale(0.98)';
        setTimeout(() => {
            e.target.style.transform = '';
        }, 150);
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + F for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.focus();
            searchInput.select();
        }
    }
    
    // Escape to clear search
    if (e.key === 'Escape') {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = '';
            filterProblems('');
        }
    }
});

// Global state
let currentData = {};
let charts = {};
let refreshInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    loadInitialData();
    setupEventListeners();
});

/**
 * Initialize dashboard components
 */
function initializeDashboard() {
    console.log('Initializing dashboard...');
    
    // Set up auto-refresh if enabled
    const autoRefresh = document.getElementById('autoRefresh');
    if (autoRefresh && autoRefresh.checked) {
        startAutoRefresh();
    }
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize syntax highlighting for code blocks
    if (typeof hljs !== 'undefined') {
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightBlock(block);
        });
    }
}

/**
 * Load initial data
 */
function loadInitialData() {
    loadStats();
    loadEvaluations();
    loadModels();
    loadCharts();
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Auto-refresh toggle
    const autoRefresh = document.getElementById('autoRefresh');
    if (autoRefresh) {
        autoRefresh.addEventListener('change', function(e) {
            if (e.target.checked) {
                startAutoRefresh();
            } else {
                stopAutoRefresh();
            }
        });
    }
    
    // Search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(handleSearch, 300));
    }
    
    // Refresh button
    const refreshBtn = document.getElementById('refreshBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshAll);
    }
}

/**
 * Start auto-refresh
 */
function startAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
    refreshInterval = setInterval(refreshAll, 30000); // 30 seconds
    console.log('Auto-refresh started');
}

/**
 * Stop auto-refresh
 */
function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
        refreshInterval = null;
        console.log('Auto-refresh stopped');
    }
}

/**
 * Refresh all data
 */
function refreshAll() {
    console.log('Refreshing all data...');
    loadStats();
    loadEvaluations();
    loadModels();
    loadCharts();
}

/**
 * Load system statistics
 */
function loadStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStats(data);
        })
        .catch(error => {
            console.error('Failed to load stats:', error);
            showNotification('Failed to load statistics', 'error');
        });
}

/**
 * Update statistics display
 */
function updateStats(stats) {
    const elements = {
        'evaluationsCount': stats.evaluations,
        'resultsCount': stats.results,
        'modelsCount': stats.models,
        'reportsCount': stats.reports,
        'diskSpace': stats.disk_space ? stats.disk_space.toFixed(2) + ' GB' : 'N/A'
    };
    
    for (const [id, value] of Object.entries(elements)) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
}

/**
 * Load evaluations list
 */
function loadEvaluations() {
    fetch('/api/evaluations')
        .then(response => response.json())
        .then(data => {
            updateEvaluationsTable(data);
        })
        .catch(error => {
            console.error('Failed to load evaluations:', error);
        });
}

/**
 * Update evaluations table
 */
function updateEvaluationsTable(evaluations) {
    const tableBody = document.getElementById('evaluationsTableBody');
    if (!tableBody) return;
    
    if (evaluations.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="6" class="text-center">No evaluations found</td></tr>';
        return;
    }
    
    let html = '';
    evaluations.forEach(evaluation => {
        const statusClass = getStatusClass(evaluation.status);
        html += `
            <tr onclick="window.location='/evaluation/${evaluation.evaluation_id}'" style="cursor: pointer;">
                <td>${evaluation.evaluation_id}</td>
                <td>${formatDate(evaluation.created_at)}</td>
                <td>${evaluation.models ? evaluation.models.join(', ') : 'N/A'}</td>
                <td>${evaluation.results_count || 0}</td>
                <td><span class="badge ${statusClass}">${evaluation.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); viewEvaluation('${evaluation.evaluation_id}')">
                        View
                    </button>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

/**
 * Load models list
 */
function loadModels() {
    fetch('/api/models')
        .then(response => response.json())
        .then(data => {
            updateModelsTable(data);
        })
        .catch(error => {
            console.error('Failed to load models:', error);
        });
}

/**
 * Update models table
 */
function updateModelsTable(models) {
    const tableBody = document.getElementById('modelsTableBody');
    if (!tableBody) return;
    
    if (models.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="5" class="text-center">No models found</td></tr>';
        return;
    }
    
    let html = '';
    models.forEach(model => {
        const statusClass = model.active ? 'badge-success' : 'badge-secondary';
        html += `
            <tr>
                <td>${model.model_id}</td>
                <td>${model.provider || 'N/A'}</td>
                <td>${model.config ? JSON.stringify(model.config) : '{}'}</td>
                <td><span class="badge ${statusClass}">${model.active ? 'Active' : 'Inactive'}</span></td>
                <td>
                    <button class="btn btn-sm btn-info" onclick="testModel('${model.model_id}')">
                        Test
                    </button>
                </td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = html;
}

/**
 * Load charts
 */
function loadCharts() {
    // Load pass rate chart
    fetch('/api/charts/pass_rate')
        .then(response => response.json())
        .then(data => {
            renderChart('passRateChart', data);
        })
        .catch(error => {
            console.error('Failed to load pass rate chart:', error);
        });
    
    // Load performance trend chart
    fetch('/api/charts/performance_trend')
        .then(response => response.json())
        .then(data => {
            renderChart('trendChart', data);
        })
        .catch(error => {
            console.error('Failed to load trend chart:', error);
        });
}

/**
 * Render a Plotly chart
 */
function renderChart(elementId, data) {
    const element = document.getElementById(elementId);
    if (!element || !data) return;
    
    if (charts[elementId]) {
        Plotly.react(elementId, data.data, data.layout);
    } else {
        charts[elementId] = Plotly.newPlot(elementId, data.data, data.layout);
    }
}

/**
 * Handle search
 */
function handleSearch(event) {
    const query = event.target.value;
    if (query.length < 2) return;
    
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(results => {
            displaySearchResults(results);
        })
        .catch(error => {
            console.error('Search failed:', error);
        });
}

/**
 * Display search results
 */
function displaySearchResults(results) {
    const container = document.getElementById('searchResults');
    if (!container) return;
    
    if (results.length === 0) {
        container.innerHTML = '<div class="text-muted">No results found</div>';
        return;
    }
    
    let html = '<div class="list-group">';
    results.forEach(result => {
        html += `
            <a href="${result.url}" class="list-group-item list-group-item-action">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${result.title}</h6>
                    <small class="text-muted">${result.type}</small>
                </div>
            </a>
        `;
    });
    html += '</div>';
    
    container.innerHTML = html;
}

/**
 * View evaluation details
 */
function viewEvaluation(evaluationId) {
    window.location.href = `/evaluation/${evaluationId}`;
}

/**
 * Test model connection
 */
function testModel(modelId) {
    fetch(`/api/models/${modelId}/test`, {
        method: 'POST'
    })
        .then(response => response.json())
        .then(data => {
            if (data.connected) {
                showNotification(`Model ${modelId} is connected`, 'success');
            } else {
                showNotification(`Model ${modelId} is not connected`, 'warning');
            }
        })
        .catch(error => {
            console.error('Failed to test model:', error);
            showNotification('Failed to test model', 'error');
        });
}

/**
 * Start new evaluation
 */
function startNewEvaluation() {
    const models = Array.from(document.querySelectorAll('input[name="models"]:checked'))
        .map(cb => cb.value);
    
    const config = {
        num_samples: parseInt(document.getElementById('numSamples').value) || 5,
        timeout: parseInt(document.getElementById('timeout').value) || 30
    };
    
    fetch('/api/evaluations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: 'current-user',
            models: models,
            dataset_id: document.getElementById('dataset').value,
            config: config
        })
    })
        .then(response => response.json())
        .then(data => {
            showNotification('Evaluation started', 'success');
            setTimeout(() => {
                window.location.href = `/evaluation/${data.evaluation_id}`;
            }, 1000);
        })
        .catch(error => {
            console.error('Failed to start evaluation:', error);
            showNotification('Failed to start evaluation', 'error');
        });
}

/**
 * Generate report
 */
function generateReport(evaluationId, format = 'html', type = 'summary') {
    fetch('/api/reports', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            evaluation_id: evaluationId,
            format: format,
            type: type
        })
    })
        .then(response => response.json())
        .then(data => {
            showNotification('Report generated', 'success');
            window.open(`/api/reports/${data.report_id}/download`);
        })
        .catch(error => {
            console.error('Failed to generate report:', error);
            showNotification('Failed to generate report', 'error');
        });
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

/**
 * Format date
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
}

/**
 * Get status CSS class
 */
function getStatusClass(status) {
    const classes = {
        'pending': 'badge-secondary',
        'running': 'badge-primary',
        'completed': 'badge-success',
        'failed': 'badge-danger',
        'cancelled': 'badge-warning'
    };
    return classes[status] || 'badge-secondary';
}

/**
 * Debounce function
 */
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

/**
 * Copy to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied to clipboard', 'success');
    }).catch(() => {
        showNotification('Failed to copy', 'error');
    });
}

/**
 * Export data
 */
function exportData(format = 'csv') {
    const data = currentData;
    
    if (format === 'csv') {
        // Convert to CSV
        let csv = '';
        if (Array.isArray(data)) {
            const headers = Object.keys(data[0] || {});
            csv += headers.join(',') + '\n';
            data.forEach(row => {
                csv += headers.map(h => row[h]).join(',') + '\n';
            });
        }
        
        downloadFile(csv, 'export.csv', 'text/csv');
    } else if (format === 'json') {
        downloadFile(JSON.stringify(data, null, 2), 'export.json', 'application/json');
    }
}

/**
 * Download file
 */
function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}

/**
 * Initialize tooltips
 */
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

/**
 * Show tooltip
 */
function showTooltip(event) {
    const element = event.target;
    const text = element.getAttribute('data-tooltip');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    tooltip.style.position = 'absolute';
    tooltip.style.top = event.pageY + 10 + 'px';
    tooltip.style.left = event.pageX + 10 + 'px';
    
    document.body.appendChild(tooltip);
    element._tooltip = tooltip;
}

/**
 * Hide tooltip
 */
function hideTooltip(event) {
    if (event.target._tooltip) {
        event.target._tooltip.remove();
        delete event.target._tooltip;
    }
}
import re

with open('orders/templates/orders/manager_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('₦', '₵')

# We can replace the inner part of dashboard-panel
pattern = r'<div class="dashboard-panel">.*?</div>\s*</div>'
replacement = """<div class="dashboard-panel">
        <div class="panel-block chart-container">
            <h3>Revenue (Last 7 Days)</h3>
            <canvas id="revenueChart"></canvas>
        </div>
        <div class="panel-block chart-container">
            <h3>Order Status</h3>
            <canvas id="statusChart"></canvas>
        </div>
        <div class="panel-block">
            <h3>Top products</h3>
            {% if top_products %}
                <ul class="status-list">
                    {% for product in top_products %}
                        <li>{{ product.item_name }} — {{ product.total_quantity }} sold</li>
                    {% endfor %}
                </ul>
            {% else %}
                <p>No paid orders found yet.</p>
            {% endif %}
        </div>
    </div>"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

css_to_add = """
.chart-container {
    position: relative;
    height: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.chart-container canvas {
    max-height: 250px;
}
"""
content = content.replace('</style>', css_to_add + '</style>')

js_block = """
{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const revCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revCtx, {
        type: 'bar',
        data: {
            labels: {{ last_7_days_labels|safe }},
            datasets: [{
                label: 'Revenue (₵)',
                data: {{ last_7_days_revenue|safe }},
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true } }
        }
    });

    const statusCtx = document.getElementById('statusChart').getContext('2d');
    new Chart(statusCtx, {
        type: 'doughnut',
        data: {
            labels: ['Pending', 'Paid', 'Processing', 'Completed', 'Cancelled'],
            datasets: [{
                data: [
                    {{ status_distribution.pending }},
                    {{ status_distribution.paid }},
                    {{ status_distribution.processing }},
                    {{ status_distribution.completed }},
                    {{ status_distribution.cancelled }}
                ],
                backgroundColor: ['#f59e0b', '#3b82f6', '#8b5cf6', '#10b981', '#ef4444'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'right' } }
        }
    });
</script>
{% endblock %}
"""

content = re.sub(r'(</style>\s*?{% endblock %})', '</style>\n{% endblock %}\n' + js_block, content)

with open('orders/templates/orders/manager_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

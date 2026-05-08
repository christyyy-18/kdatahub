from pathlib import Path

root = Path(__file__).resolve().parent
render_files = [root / 'render.yaml', root / 'RENDER_DEPLOYMENT_GUIDE.md']
for p in render_files:
    if p.exists():
        p.unlink()
        print(f'Deleted {p.name}')

patch_files = [
    root / 'DEPLOYMENT_READY.md',
    root / 'DEPLOYMENT_CHECKLIST.md',
    root / 'ENVIRONMENT_VARIABLES.md',
    root / 'PRODUCTION_READY.md',
    root / 'PAYSTACK_SETUP.md',
    root / 'COMPLETION_SUMMARY.md',
    root / '.env.example',
]
replacements = [
    ('RENDER_DEPLOYMENT_GUIDE.md', 'deployment guide'),
    ('render.yaml', 'deployment manifest'),
    ('Render environment', 'deployment environment'),
    ('Render dashboard', 'deployment dashboard'),
    ('Render domain', 'deployment domain'),
    ('Render.com', 'your deployment provider'),
    ('render.com', 'your deployment provider'),
    ('https://dashboard.render.com/', 'your deployment dashboard'),
    ('https://render.com/docs', 'your deployment provider docs'),
    ('https://render.com/docs/postgres', 'your database docs'),
    ('https://render.com/signup', 'your deployment provider signup page'),
    ('ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com', 'ALLOWED_HOSTS=localhost,127.0.0.1'),
    ('BASE_DOMAIN=https://kdatahub.onrender.com', 'BASE_DOMAIN=https://your-deployment-domain.com'),
    ('kdatahub.onrender.com', 'your deployment domain'),
    ('YOUR-DOMAIN.onrender.com', 'your deployment domain'),
    ('https://YOUR-DOMAIN.onrender.com', 'https://your deployment domain'),
    ('https://kdatahub.onrender.com', 'https://your deployment domain'),
    ('https://your-deployment-domain.com/payments/webhook/paystack/', 'https://your deployment domain/payments/webhook/paystack/'),
    ('# 3. For production (Render), set these in the Render dashboard instead', '# 3. For production, set these in your deployment environment instead'),
    ('## Production Environment (Render)', '## Production Environment'),
    ('## Complete Render Environment Variables Checklist', '## Complete Production Environment Variables Checklist'),
    ('Use this as a reference when setting up Render:', 'Use this as a reference when setting up your deployment environment:'),
    ('Target Platform: Render.com', 'Target Platform: Supabase / deployment provider'),
    ('Create Render account', 'Create a deployment account'),
    ('Deploy to Render', 'Deploy to your hosting provider'),
    ('After deployment to Render:', 'After deployment:'),
    ('On Render, check logs:', 'Check your deployment logs:'),
    ('- Render Docs: https://render.com/docs', '- Deployment provider docs'),
    ('➡️ Add to Render Environment:', '➡️ Add to environment variables:'),
    ('Your Render domain', 'your deployment domain'),
    ('www.render.com', 'your deployment provider'),
    ('Render (App)', 'Deployment provider (App)'),
    ('Render (PostgreSQL)', 'Production PostgreSQL'),
    ('Render environment variables', 'production environment variables'),
    ('render.yaml created for IaC deployment', 'deployment manifest created for IaC deployment'),
]
for f in patch_files:
    if not f.exists():
        continue
    text = f.read_text(encoding='utf-8')
    for old, new in replacements:
        text = text.replace(old, new)
    text = text.replace('.onrender.com', 'your deployment domain')
    f.write_text(text, encoding='utf-8')
    print(f'Patched {f.name}')

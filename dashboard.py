import * as path from 'path'
import { Dashboard } from 'checkly/constructs'

new Dashboard('acme-dashboard-1', {
  header: 'ACME production',
  description: 'service availability and response times',
  tags: ['prod', 'api'],
  logo: 'https://assets.acme.com/images/acme-logo.png',
  customUrl: 'acme-status-page.com',
  customCSS: {
    entrypoint: path.join(__dirname, 'dashboard.css'),
  }
})

import fs from 'fs';
import { parse } from 'node-html-parser';

function khmlToHtml(khmlString) {
  return khmlString
    .replaceAll('<page', '<div class="page"')
    .replaceAll('</page>', '</div>')
    .replaceAll('<feed', '<section class="feed"')
    .replaceAll('</feed>', '</section>')
    .replaceAll('<post', '<article class="post"')
    .replaceAll('</post>', '</article>');
}

const khml = fs.readFileSync('index.khml', 'utf-8');
const html = khmlToHtml(khml);
fs.writeFileSync('index.html', html);
console.log('✅ KHML converted to HTML');

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 800 });
  
  await page.goto('https://tony.automatisationboost.com', { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // Check if contact section exists
  const hasContact = await page.evaluate(() => !!document.getElementById('contact'));
  const sections = await page.evaluate(() => {
    const secs = document.querySelectorAll('section');
    return Array.from(secs).map(s => ({
      id: s.id,
      classes: s.className.substring(0, 60),
      text: s.textContent?.trim().substring(0, 80)
    }));
  });

  console.log('Contact section exists:', hasContact);
  console.log('All sections:', JSON.stringify(sections, null, 2));

  // Scroll to bottom to load lazy content
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(1000);

  // Take screenshots
  await page.screenshot({ path: '/tmp/tony-full.png', fullPage: true });
  
  // Try to scroll to contact
  if (hasContact) {
    await page.evaluate(() => document.getElementById('contact').scrollIntoView());
    await page.waitForTimeout(500);
    await page.screenshot({ path: '/tmp/tony-contact.png' });
    console.log('Contact section visible — screenshot saved');
  }

  const pageHeight = await page.evaluate(() => document.body.scrollHeight);
  console.log('Page height:', pageHeight);

  await browser.close();
})();

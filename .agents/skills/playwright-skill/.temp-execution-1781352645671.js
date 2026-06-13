const { chromium } = require('playwright');

const TARGET_URL = 'http://a13ltxovqte9j9i7ej2l5pa3.158.220.127.234.sslip.io';

(async () => {
  console.log(`🌐 Testing: ${TARGET_URL}`);
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  try {
    await page.goto(TARGET_URL, { waitUntil: 'networkidle', timeout: 15000 });
    console.log('✅ Page loaded');

    // Attendre que l'image se charge
    await page.waitForTimeout(2000);

    // Vérifier si l'image portrait existe
    const portraitImg = await page.locator('img[alt="Tony Payet"]').first();
    const isVisible = await portraitImg.isVisible();
    
    console.log(`\n📸 Image portrait (alt="Tony Payet"): ${isVisible ? '✅ VISIBLE' : '❌ PAS VISIBLE'}`);

    if (isVisible) {
      const src = await portraitImg.getAttribute('src');
      console.log(`   Source: ${src}`);
    }

    // Chercher toutes les images sur la page
    const allImages = await page.locator('img').all();
    console.log(`\n📊 Total d'images trouvées: ${allImages.length}`);
    
    for (let i = 0; i < allImages.length; i++) {
      const img = allImages[i];
      const src = await img.getAttribute('src');
      const alt = await img.getAttribute('alt');
      const visible = await img.isVisible();
      console.log(`   [${i+1}] ${visible ? '✅' : '❌'} ${alt || '(no alt)'} -> ${src}`);
    }

    // Prendre une screenshot
    await page.screenshot({ 
      path: '/tmp/hero-screenshot.png', 
      fullPage: true 
    });
    console.log('\n✅ Screenshot sauvegardée: /tmp/hero-screenshot.png');

  } catch (error) {
    console.error('❌ Erreur:', error.message);
  } finally {
    await browser.close();
  }
})();

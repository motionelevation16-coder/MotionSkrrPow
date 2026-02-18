import sharp from 'sharp';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const publicDir = join(__dirname, '..', 'public');

async function removeWhiteBackground(inputPath, outputPath) {
  try {
    // Read the image
    const image = sharp(inputPath);
    const { width, height } = await image.metadata();
    
    // Get raw pixel data
    const { data, info } = await image
      .raw()
      .toBuffer({ resolveWithObject: true });
    
    // Create alpha channel - make white/near-white pixels transparent
    const pixels = new Uint8Array(width * height * 4);
    
    for (let i = 0; i < width * height; i++) {
      const r = data[i * 3];
      const g = data[i * 3 + 1];
      const b = data[i * 3 + 2];
      
      pixels[i * 4] = r;
      pixels[i * 4 + 1] = g;
      pixels[i * 4 + 2] = b;
      
      // If pixel is very light (close to white), make it transparent
      // Using a threshold - if all RGB values are > 240, consider it white
      const isWhite = r > 245 && g > 245 && b > 245;
      // Also check for near-white with slight color tint
      const isNearWhite = r > 235 && g > 235 && b > 235 && 
                          Math.abs(r - g) < 15 && Math.abs(g - b) < 15 && Math.abs(r - b) < 15;
      
      pixels[i * 4 + 3] = (isWhite || isNearWhite) ? 0 : 255;
    }
    
    // Save as PNG with transparency
    await sharp(pixels, {
      raw: {
        width,
        height,
        channels: 4
      }
    })
    .png()
    .toFile(outputPath);
    
    console.log(`✅ Processed: ${outputPath}`);
  } catch (error) {
    console.error(`❌ Error processing ${inputPath}:`, error.message);
  }
}

// Process both logos
const logos = [
  { input: 'logo-reading.jpg', output: 'logo-reading.png' },
  { input: 'logo-hover.jpg', output: 'logo-hover.png' }
];

for (const logo of logos) {
  await removeWhiteBackground(
    join(publicDir, logo.input),
    join(publicDir, logo.output)
  );
}

console.log('\n🦞 Done! Logos now have transparent backgrounds.');

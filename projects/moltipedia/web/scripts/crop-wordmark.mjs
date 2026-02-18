import sharp from 'sharp';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const publicDir = join(__dirname, '..', 'public');

async function cropWordmark() {
  const inputPath = join(publicDir, 'moltipedia-wordmark.png');
  const outputPath = join(publicDir, 'moltipedia-wordmark-cropped.png');
  
  // Trim whitespace automatically
  await sharp(inputPath)
    .trim() // Removes border pixels that match the top-left pixel
    .toFile(outputPath);
  
  // Get info about the cropped image
  const info = await sharp(outputPath).metadata();
  console.log(`✅ Cropped wordmark: ${info.width}x${info.height}`);
  
  // Replace original
  await sharp(outputPath).toFile(inputPath);
  console.log('✅ Replaced original wordmark with cropped version');
}

cropWordmark();

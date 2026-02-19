// Crystal Match - Addictive Matching Game
// Built with dopamine engineering 🎰

const GRID_SIZE = 8;
const GEM_TYPES = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'];
const GEM_ICONS = ['💎', '🔮', '💚', '⭐', '🔯', '🧡'];
const INITIAL_MOVES = 30;

// Audio Context for sounds
let audioCtx = null;

// Game state
let grid = [];
let score = 0;
let combo = 1;
let moves = INITIAL_MOVES;
let streak = 0;
let selectedGem = null;
let isProcessing = false;

// DOM Elements
const boardEl = document.getElementById('board');
const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const movesEl = document.getElementById('moves');
const streakEl = document.getElementById('streak');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over');
const finalScoreEl = document.getElementById('final-score');
const comboPopup = document.getElementById('combo-popup');
const comboText = document.getElementById('combo-text');
const particlesEl = document.getElementById('particles');

// Initialize audio context on first interaction
function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

// Sound effects using Web Audio API
function playSound(type) {
    if (!audioCtx) return;
    
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    switch(type) {
        case 'match':
            oscillator.frequency.setValueAtTime(523, audioCtx.currentTime); // C5
            oscillator.frequency.exponentialRampToValueAtTime(784, audioCtx.currentTime + 0.1);
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
            oscillator.type = 'sine';
            break;
            
        case 'combo':
            oscillator.frequency.setValueAtTime(523, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(1047, audioCtx.currentTime + 0.15);
            gainNode.gain.setValueAtTime(0.4, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
            oscillator.type = 'square';
            break;
            
        case 'select':
            oscillator.frequency.setValueAtTime(440, audioCtx.currentTime);
            gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);
            oscillator.type = 'sine';
            break;
            
        case 'swap':
            oscillator.frequency.setValueAtTime(330, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.1);
            gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
            oscillator.type = 'triangle';
            break;

        case 'bigwin':
            // Celebratory arpeggio
            const notes = [523, 659, 784, 1047];
            notes.forEach((freq, i) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime + i * 0.1);
                gain.gain.setValueAtTime(0.3, audioCtx.currentTime + i * 0.1);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + i * 0.1 + 0.2);
                osc.type = 'sine';
                osc.start(audioCtx.currentTime + i * 0.1);
                osc.stop(audioCtx.currentTime + i * 0.1 + 0.25);
            });
            return;
    }
    
    oscillator.start(audioCtx.currentTime);
    oscillator.stop(audioCtx.currentTime + 0.2);
}

// Create particles
function createParticles(x, y, color, count = 8) {
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle sparkle';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.background = color;
        
        const angle = (Math.PI * 2 * i) / count;
        const distance = 40 + Math.random() * 40;
        const dx = Math.cos(angle) * distance;
        const dy = Math.sin(angle) * distance;
        
        particle.style.setProperty('--dx', dx + 'px');
        particle.style.setProperty('--dy', dy + 'px');
        
        particlesEl.appendChild(particle);
        
        setTimeout(() => particle.remove(), 800);
    }
}

// Create coin animation
function createCoinBurst(x, y) {
    for (let i = 0; i < 5; i++) {
        const coin = document.createElement('div');
        coin.className = 'particle coin';
        coin.textContent = '💰';
        coin.style.left = (x + Math.random() * 30 - 15) + 'px';
        coin.style.top = y + 'px';
        
        particlesEl.appendChild(coin);
        
        setTimeout(() => coin.remove(), 1000);
    }
}

// Create score popup
function createScorePopup(x, y, points) {
    const popup = document.createElement('div');
    popup.className = 'score-popup';
    popup.textContent = '+' + points;
    popup.style.left = x + 'px';
    popup.style.top = y + 'px';
    
    particlesEl.appendChild(popup);
    
    setTimeout(() => popup.remove(), 800);
}

// Screen shake
function screenShake(intensity = 1) {
    const board = document.getElementById('board-wrapper');
    board.classList.add('shake');
    setTimeout(() => board.classList.remove('shake'), 300);
}

// Show combo popup
function showComboPopup(text) {
    comboText.textContent = text;
    comboPopup.classList.remove('hidden');
    comboPopup.style.animation = 'none';
    comboPopup.offsetHeight; // Force reflow
    comboPopup.style.animation = 'comboPopup 0.8s ease-out forwards';
    
    setTimeout(() => comboPopup.classList.add('hidden'), 800);
}

// Initialize grid
function initGrid() {
    grid = [];
    for (let row = 0; row < GRID_SIZE; row++) {
        grid[row] = [];
        for (let col = 0; col < GRID_SIZE; col++) {
            let type;
            // Avoid creating matches on init
            do {
                type = Math.floor(Math.random() * GEM_TYPES.length);
            } while (
                (col >= 2 && grid[row][col-1] === type && grid[row][col-2] === type) ||
                (row >= 2 && grid[row-1][col] === type && grid[row-2][col] === type)
            );
            grid[row][col] = type;
        }
    }
}

// Render grid
function renderGrid() {
    boardEl.innerHTML = '';
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            const gem = document.createElement('div');
            const type = grid[row][col];
            gem.className = `gem gem-${GEM_TYPES[type]}`;
            gem.textContent = GEM_ICONS[type];
            gem.dataset.row = row;
            gem.dataset.col = col;
            
            gem.addEventListener('click', () => handleGemClick(row, col));
            gem.addEventListener('touchstart', (e) => {
                e.preventDefault();
                handleGemClick(row, col);
            });
            
            boardEl.appendChild(gem);
        }
    }
}

// Handle gem click
function handleGemClick(row, col) {
    if (isProcessing || moves <= 0) return;
    
    initAudio();
    
    const gems = document.querySelectorAll('.gem');
    const index = row * GRID_SIZE + col;
    const gem = gems[index];
    
    if (selectedGem === null) {
        // Select gem
        selectedGem = { row, col };
        gem.classList.add('selected');
        playSound('select');
    } else if (selectedGem.row === row && selectedGem.col === col) {
        // Deselect
        gem.classList.remove('selected');
        selectedGem = null;
    } else {
        // Check if adjacent
        const dr = Math.abs(selectedGem.row - row);
        const dc = Math.abs(selectedGem.col - col);
        
        if ((dr === 1 && dc === 0) || (dr === 0 && dc === 1)) {
            // Swap
            const prevGem = gems[selectedGem.row * GRID_SIZE + selectedGem.col];
            prevGem.classList.remove('selected');
            
            swapGems(selectedGem.row, selectedGem.col, row, col);
            selectedGem = null;
        } else {
            // Select new gem
            const prevGem = gems[selectedGem.row * GRID_SIZE + selectedGem.col];
            prevGem.classList.remove('selected');
            selectedGem = { row, col };
            gem.classList.add('selected');
            playSound('select');
        }
    }
}

// Swap gems
async function swapGems(r1, c1, r2, c2) {
    isProcessing = true;
    playSound('swap');
    
    // Swap in grid
    [grid[r1][c1], grid[r2][c2]] = [grid[r2][c2], grid[r1][c1]];
    renderGrid();
    
    // Check for matches
    const matches = findMatches();
    
    if (matches.length > 0) {
        moves--;
        movesEl.textContent = moves;
        combo = 1;
        
        await processMatches();
        
        // Check for game over
        if (moves <= 0) {
            endGame();
        }
    } else {
        // Swap back
        [grid[r1][c1], grid[r2][c2]] = [grid[r2][c2], grid[r1][c1]];
        renderGrid();
    }
    
    isProcessing = false;
}

// Find all matches
function findMatches() {
    const matches = new Set();
    
    // Horizontal matches
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE - 2; col++) {
            const type = grid[row][col];
            if (type !== -1 && grid[row][col+1] === type && grid[row][col+2] === type) {
                matches.add(`${row},${col}`);
                matches.add(`${row},${col+1}`);
                matches.add(`${row},${col+2}`);
                
                // Check for longer matches
                let i = col + 3;
                while (i < GRID_SIZE && grid[row][i] === type) {
                    matches.add(`${row},${i}`);
                    i++;
                }
            }
        }
    }
    
    // Vertical matches
    for (let col = 0; col < GRID_SIZE; col++) {
        for (let row = 0; row < GRID_SIZE - 2; row++) {
            const type = grid[row][col];
            if (type !== -1 && grid[row+1][col] === type && grid[row+2][col] === type) {
                matches.add(`${row},${col}`);
                matches.add(`${row+1},${col}`);
                matches.add(`${row+2},${col}`);
                
                // Check for longer matches
                let i = row + 3;
                while (i < GRID_SIZE && grid[i][col] === type) {
                    matches.add(`${i},${col}`);
                    i++;
                }
            }
        }
    }
    
    return Array.from(matches).map(pos => {
        const [row, col] = pos.split(',').map(Number);
        return { row, col };
    });
}

// Process matches
async function processMatches() {
    let matches = findMatches();
    let cascadeCount = 0;
    
    while (matches.length > 0) {
        cascadeCount++;
        
        // Calculate points
        const basePoints = matches.length * 10;
        const comboMultiplier = combo;
        const cascadeBonus = cascadeCount > 1 ? (cascadeCount - 1) * 0.5 : 0;
        const totalPoints = Math.floor(basePoints * comboMultiplier * (1 + cascadeBonus));
        
        // Update score
        score += totalPoints;
        scoreEl.textContent = score.toLocaleString();
        
        // Update combo
        comboEl.textContent = `x${combo}`;
        
        // Visual and audio feedback
        if (matches.length >= 4) {
            playSound('combo');
            screenShake(matches.length >= 6 ? 2 : 1);
            
            if (matches.length >= 6) {
                showComboPopup('🔥 AMAZING!');
                createCoinBurst(window.innerWidth / 2, window.innerHeight / 2);
            } else {
                showComboPopup('✨ GREAT!');
            }
        } else {
            playSound('match');
        }
        
        // Remove matched gems with animation
        const gems = document.querySelectorAll('.gem');
        matches.forEach(({ row, col }) => {
            const index = row * GRID_SIZE + col;
            const gem = gems[index];
            const rect = gem.getBoundingClientRect();
            const boardRect = boardEl.getBoundingClientRect();
            
            gem.classList.add('matched');
            
            // Create particles
            const x = rect.left - boardRect.left + rect.width / 2;
            const y = rect.top - boardRect.top + rect.height / 2;
            const color = getComputedStyle(gem).background.match(/rgb\([^)]+\)/)?.[0] || '#fff';
            createParticles(x, y, color);
            createScorePopup(x, y, Math.floor(totalPoints / matches.length));
            
            grid[row][col] = -1;
        });
        
        // Update streak
        streak++;
        streakEl.textContent = streak;
        
        await delay(300);
        
        // Drop gems
        dropGems();
        renderGrid();
        
        await delay(200);
        
        // Fill empty spaces
        fillGems();
        renderGrid();
        
        await delay(200);
        
        // Increment combo
        combo++;
        
        // Find new matches
        matches = findMatches();
    }
    
    // Reset combo
    combo = 1;
    comboEl.textContent = 'x1';
    
    // Big win celebration
    if (cascadeCount >= 3) {
        playSound('bigwin');
        showComboPopup('🎰 JACKPOT!');
        screenShake(2);
    }
}

// Drop gems
function dropGems() {
    for (let col = 0; col < GRID_SIZE; col++) {
        let emptyRow = GRID_SIZE - 1;
        
        for (let row = GRID_SIZE - 1; row >= 0; row--) {
            if (grid[row][col] !== -1) {
                if (row !== emptyRow) {
                    grid[emptyRow][col] = grid[row][col];
                    grid[row][col] = -1;
                }
                emptyRow--;
            }
        }
    }
}

// Fill empty spaces
function fillGems() {
    for (let col = 0; col < GRID_SIZE; col++) {
        for (let row = 0; row < GRID_SIZE; row++) {
            if (grid[row][col] === -1) {
                grid[row][col] = Math.floor(Math.random() * GEM_TYPES.length);
            }
        }
    }
}

// Shuffle board
function shuffleBoard() {
    if (isProcessing) return;
    
    initAudio();
    playSound('swap');
    screenShake();
    
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            const r2 = Math.floor(Math.random() * GRID_SIZE);
            const c2 = Math.floor(Math.random() * GRID_SIZE);
            [grid[row][col], grid[r2][c2]] = [grid[r2][c2], grid[row][col]];
        }
    }
    
    // Ensure no matches exist
    let matches = findMatches();
    while (matches.length > 0) {
        matches.forEach(({ row, col }) => {
            grid[row][col] = Math.floor(Math.random() * GEM_TYPES.length);
        });
        matches = findMatches();
    }
    
    renderGrid();
}

// End game
function endGame() {
    finalScoreEl.textContent = score.toLocaleString();
    gameOverScreen.classList.remove('hidden');
    playSound('bigwin');
}

// Start game
function startGame() {
    score = 0;
    moves = INITIAL_MOVES;
    combo = 1;
    streak = 0;
    selectedGem = null;
    isProcessing = false;
    
    scoreEl.textContent = '0';
    movesEl.textContent = moves;
    comboEl.textContent = 'x1';
    streakEl.textContent = '0';
    
    initGrid();
    renderGrid();
    
    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    
    initAudio();
}

// Utility
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Event listeners
document.getElementById('start-btn').addEventListener('click', startGame);
document.getElementById('play-again').addEventListener('click', startGame);
document.getElementById('shuffle-btn').addEventListener('click', shuffleBoard);

// Prevent zoom on double tap
document.addEventListener('touchstart', (e) => {
    if (e.touches.length > 1) {
        e.preventDefault();
    }
}, { passive: false });

let lastTouchEnd = 0;
document.addEventListener('touchend', (e) => {
    const now = Date.now();
    if (now - lastTouchEnd <= 300) {
        e.preventDefault();
    }
    lastTouchEnd = now;
}, false);

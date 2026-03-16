// Crystal Match - Addictive Matching Game v2.0
// Built with dopamine engineering 🎰

const GRID_SIZE = 8;
const GEM_TYPES = ['red', 'blue', 'green', 'yellow', 'purple', 'orange'];
const GEM_ICONS = ['💎', '🔮', '💚', '⭐', '🔯', '🧡'];
const SPECIAL_ICONS = {
    bomb: '💣',
    lightning: '⚡',
    rainbow: '🌈'
};

// Audio Context for sounds
let audioCtx = null;

// Game state
let grid = [];
let score = 0;
let combo = 1;
let moves = 0;
let streak = 0;
let level = 1;
let levelGoal = 0;
let levelScore = 0;
let selectedGem = null;
let isProcessing = false;
let totalMatches = 0;

// Level configuration
const LEVELS = [
    { moves: 20, goal: 1000, name: "Getting Started" },
    { moves: 18, goal: 2000, name: "Warming Up" },
    { moves: 18, goal: 3500, name: "Finding Rhythm" },
    { moves: 16, goal: 5000, name: "Combo Master" },
    { moves: 16, goal: 7000, name: "Crystal Hunter" },
    { moves: 15, goal: 10000, name: "Gem Crusher" },
    { moves: 15, goal: 13000, name: "Sparkle Storm" },
    { moves: 14, goal: 17000, name: "Diamond Mind" },
    { moves: 14, goal: 22000, name: "Jewel King" },
    { moves: 12, goal: 30000, name: "💎 LEGENDARY" }
];

// DOM Elements
const boardEl = document.getElementById('board');
const scoreEl = document.getElementById('score');
const comboEl = document.getElementById('combo');
const movesEl = document.getElementById('moves');
const streakEl = document.getElementById('streak');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over');
const levelCompleteScreen = document.getElementById('level-complete');
const finalScoreEl = document.getElementById('final-score');
const comboPopup = document.getElementById('combo-popup');
const comboText = document.getElementById('combo-text');
const particlesEl = document.getElementById('particles');
const levelEl = document.getElementById('level');
const goalEl = document.getElementById('goal');
const progressBar = document.getElementById('progress-fill');

// Initialize audio context on first interaction
function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

// Sound effects using Web Audio API
function playSound(type, pitch = 1) {
    if (!audioCtx) return;
    
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    const baseFreq = 523 * pitch;
    
    switch(type) {
        case 'match':
            oscillator.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(baseFreq * 1.5, audioCtx.currentTime + 0.1);
            gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
            oscillator.type = 'sine';
            break;
            
        case 'combo':
            oscillator.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(baseFreq * 2, audioCtx.currentTime + 0.15);
            gainNode.gain.setValueAtTime(0.4, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.2);
            oscillator.type = 'square';
            break;
            
        case 'select':
            oscillator.frequency.setValueAtTime(440, audioCtx.currentTime);
            gainNode.gain.setValueAtTime(0.15, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
            oscillator.type = 'sine';
            break;
            
        case 'swap':
            oscillator.frequency.setValueAtTime(330, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.1);
            gainNode.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.12);
            oscillator.type = 'triangle';
            break;
            
        case 'powerup':
            // Rising arpeggio
            const notes = [523, 659, 784, 1047, 1318];
            notes.forEach((freq, i) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime + i * 0.05);
                gain.gain.setValueAtTime(0.25, audioCtx.currentTime + i * 0.05);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + i * 0.05 + 0.15);
                osc.type = 'sine';
                osc.start(audioCtx.currentTime + i * 0.05);
                osc.stop(audioCtx.currentTime + i * 0.05 + 0.2);
            });
            return;
            
        case 'explosion':
            // Deep boom
            oscillator.frequency.setValueAtTime(150, audioCtx.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(30, audioCtx.currentTime + 0.3);
            gainNode.gain.setValueAtTime(0.5, audioCtx.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
            oscillator.type = 'sawtooth';
            break;

        case 'bigwin':
            // Celebratory arpeggio
            const winNotes = [523, 659, 784, 1047];
            winNotes.forEach((freq, i) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime + i * 0.1);
                gain.gain.setValueAtTime(0.3, audioCtx.currentTime + i * 0.1);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + i * 0.1 + 0.3);
                osc.type = 'sine';
                osc.start(audioCtx.currentTime + i * 0.1);
                osc.stop(audioCtx.currentTime + i * 0.1 + 0.35);
            });
            return;
            
        case 'levelup':
            // Epic fanfare
            const fanfare = [523, 659, 784, 1047, 784, 1047, 1318];
            fanfare.forEach((freq, i) => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.frequency.setValueAtTime(freq, audioCtx.currentTime + i * 0.12);
                gain.gain.setValueAtTime(0.35, audioCtx.currentTime + i * 0.12);
                gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + i * 0.12 + 0.25);
                osc.type = i < 4 ? 'sine' : 'square';
                osc.start(audioCtx.currentTime + i * 0.12);
                osc.stop(audioCtx.currentTime + i * 0.12 + 0.3);
            });
            return;
    }
    
    oscillator.start(audioCtx.currentTime);
    oscillator.stop(audioCtx.currentTime + 0.4);
}

// Create particles
function createParticles(x, y, color, count = 12) {
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle sparkle';
        particle.style.left = x + 'px';
        particle.style.top = y + 'px';
        particle.style.background = color;
        particle.style.width = (6 + Math.random() * 8) + 'px';
        particle.style.height = particle.style.width;
        
        const angle = (Math.PI * 2 * i) / count + Math.random() * 0.5;
        const distance = 50 + Math.random() * 60;
        const dx = Math.cos(angle) * distance;
        const dy = Math.sin(angle) * distance;
        
        particle.style.setProperty('--dx', dx + 'px');
        particle.style.setProperty('--dy', dy + 'px');
        
        particlesEl.appendChild(particle);
        
        setTimeout(() => particle.remove(), 800);
    }
}

// Create explosion effect
function createExplosion(x, y) {
    // Ring effect
    const ring = document.createElement('div');
    ring.className = 'explosion-ring';
    ring.style.left = x + 'px';
    ring.style.top = y + 'px';
    particlesEl.appendChild(ring);
    setTimeout(() => ring.remove(), 500);
    
    // Lots of particles
    createParticles(x, y, '#ffd93d', 20);
    createParticles(x, y, '#ff6b6b', 15);
    createParticles(x, y, '#4ecdc4', 15);
}

// Create coin animation
function createCoinBurst(x, y, count = 8) {
    for (let i = 0; i < count; i++) {
        const coin = document.createElement('div');
        coin.className = 'particle coin';
        coin.textContent = ['💰', '💎', '✨', '⭐'][Math.floor(Math.random() * 4)];
        coin.style.left = (x + Math.random() * 40 - 20) + 'px';
        coin.style.top = y + 'px';
        coin.style.animationDelay = (i * 0.05) + 's';
        
        particlesEl.appendChild(coin);
        
        setTimeout(() => coin.remove(), 1000);
    }
}

// Create score popup
function createScorePopup(x, y, points, isSpecial = false) {
    const popup = document.createElement('div');
    popup.className = 'score-popup' + (isSpecial ? ' special' : '');
    popup.textContent = '+' + points.toLocaleString();
    popup.style.left = x + 'px';
    popup.style.top = y + 'px';
    
    particlesEl.appendChild(popup);
    
    setTimeout(() => popup.remove(), 900);
}

// Screen shake
function screenShake(intensity = 1) {
    const board = document.getElementById('board-wrapper');
    board.style.setProperty('--shake-intensity', intensity);
    board.classList.add('shake');
    setTimeout(() => board.classList.remove('shake'), 300 * intensity);
}

// Show combo popup
function showComboPopup(text, color = '#ffd93d') {
    comboText.textContent = text;
    comboText.style.color = color;
    comboPopup.classList.remove('hidden');
    comboPopup.style.animation = 'none';
    comboPopup.offsetHeight; // Force reflow
    comboPopup.style.animation = 'comboPopup 0.8s ease-out forwards';
    
    setTimeout(() => comboPopup.classList.add('hidden'), 800);
}

// Update progress bar
function updateProgress() {
    const progress = Math.min((levelScore / levelGoal) * 100, 100);
    if (progressBar) {
        progressBar.style.width = progress + '%';
        
        // Glow effect when close to goal
        if (progress >= 80) {
            progressBar.classList.add('pulse-glow');
        } else {
            progressBar.classList.remove('pulse-glow');
        }
    }
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
                (col >= 2 && getGemType(grid[row][col-1]) === type && getGemType(grid[row][col-2]) === type) ||
                (row >= 2 && getGemType(grid[row-1][col]) === type && getGemType(grid[row-2][col]) === type)
            );
            grid[row][col] = { type, special: null };
        }
    }
}

// Get gem type (handles special gems)
function getGemType(gem) {
    if (!gem) return -1;
    if (gem.special === 'rainbow') return -2; // Matches anything
    return gem.type;
}

// Render grid
function renderGrid() {
    boardEl.innerHTML = '';
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            const gem = document.createElement('div');
            const gemData = grid[row][col];
            const type = gemData.type;
            
            gem.className = `gem gem-${GEM_TYPES[type]}`;
            
            // Special gem styling
            if (gemData.special === 'bomb') {
                gem.classList.add('special-bomb');
                gem.textContent = SPECIAL_ICONS.bomb;
            } else if (gemData.special === 'lightning') {
                gem.classList.add('special-lightning');
                gem.textContent = SPECIAL_ICONS.lightning;
            } else if (gemData.special === 'rainbow') {
                gem.classList.add('special-rainbow');
                gem.textContent = SPECIAL_ICONS.rainbow;
            } else {
                gem.textContent = GEM_ICONS[type];
            }
            
            gem.dataset.row = row;
            gem.dataset.col = col;
            
            gem.addEventListener('click', () => handleGemClick(row, col));
            gem.addEventListener('touchstart', (e) => {
                e.preventDefault();
                handleGemClick(row, col);
            }, { passive: false });
            
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
        
        // Check for level complete
        if (levelScore >= levelGoal) {
            await delay(500);
            levelComplete();
        }
        // Check for game over
        else if (moves <= 0) {
            await delay(500);
            endGame();
        }
    } else {
        // Swap back with "almost" tease
        await delay(150);
        [grid[r1][c1], grid[r2][c2]] = [grid[r2][c2], grid[r1][c1]];
        renderGrid();
        
        // Near-miss tease - highlight potential matches
        highlightNearMiss(r1, c1);
        highlightNearMiss(r2, c2);
    }
    
    isProcessing = false;
}

// Highlight near-miss gems
function highlightNearMiss(row, col) {
    const gems = document.querySelectorAll('.gem');
    const index = row * GRID_SIZE + col;
    const gem = gems[index];
    
    if (gem) {
        gem.classList.add('near-miss');
        setTimeout(() => gem.classList.remove('near-miss'), 500);
    }
}

// Find all matches
function findMatches() {
    const matches = [];
    const visited = new Set();
    
    // Horizontal matches
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE - 2; col++) {
            const type = getGemType(grid[row][col]);
            if (type === -1) continue;
            
            const match = [{ row, col }];
            let i = col + 1;
            
            while (i < GRID_SIZE) {
                const nextType = getGemType(grid[row][i]);
                if (nextType === type || nextType === -2 || type === -2) {
                    match.push({ row, col: i });
                    i++;
                } else {
                    break;
                }
            }
            
            if (match.length >= 3) {
                const key = match.map(m => `${m.row},${m.col}`).join('|');
                if (!visited.has(key)) {
                    visited.add(key);
                    matches.push({ gems: match, direction: 'horizontal' });
                }
                col = i - 1;
            }
        }
    }
    
    // Vertical matches
    for (let col = 0; col < GRID_SIZE; col++) {
        for (let row = 0; row < GRID_SIZE - 2; row++) {
            const type = getGemType(grid[row][col]);
            if (type === -1) continue;
            
            const match = [{ row, col }];
            let i = row + 1;
            
            while (i < GRID_SIZE) {
                const nextType = getGemType(grid[i][col]);
                if (nextType === type || nextType === -2 || type === -2) {
                    match.push({ row: i, col });
                    i++;
                } else {
                    break;
                }
            }
            
            if (match.length >= 3) {
                const existing = matches.find(m => 
                    m.gems.some(g => match.some(mg => mg.row === g.row && mg.col === g.col))
                );
                if (!existing) {
                    matches.push({ gems: match, direction: 'vertical' });
                }
                row = i - 1;
            }
        }
    }
    
    return matches;
}

// Process matches
async function processMatches() {
    let allMatches = findMatches();
    let cascadeCount = 0;
    
    while (allMatches.length > 0) {
        cascadeCount++;
        
        // Flatten all matched positions
        const matchedPositions = new Set();
        const specialsToCreate = [];
        
        for (const match of allMatches) {
            // Check for special gem creation
            if (match.gems.length === 4) {
                // Create bomb at swap position or center
                const center = match.gems[Math.floor(match.gems.length / 2)];
                specialsToCreate.push({ 
                    row: center.row, 
                    col: center.col, 
                    type: grid[center.row][center.col].type,
                    special: 'bomb' 
                });
            } else if (match.gems.length >= 5) {
                // Create rainbow at center
                const center = match.gems[Math.floor(match.gems.length / 2)];
                specialsToCreate.push({ 
                    row: center.row, 
                    col: center.col, 
                    type: grid[center.row][center.col].type,
                    special: 'rainbow' 
                });
            }
            
            match.gems.forEach(g => matchedPositions.add(`${g.row},${g.col}`));
        }
        
        const matchCount = matchedPositions.size;
        totalMatches += matchCount;
        
        // Calculate points with casino-style multipliers
        const basePoints = matchCount * 10;
        const comboMultiplier = Math.pow(1.5, combo - 1);
        const cascadeBonus = cascadeCount > 1 ? Math.pow(1.3, cascadeCount - 1) : 1;
        const matchBonus = matchCount > 3 ? Math.pow(1.2, matchCount - 3) : 1;
        const totalPoints = Math.floor(basePoints * comboMultiplier * cascadeBonus * matchBonus);
        
        // Update scores
        score += totalPoints;
        levelScore += totalPoints;
        scoreEl.textContent = score.toLocaleString();
        updateProgress();
        
        // Update combo display
        comboEl.textContent = `x${combo}`;
        if (combo >= 3) {
            comboEl.classList.add('combo-high');
        } else {
            comboEl.classList.remove('combo-high');
        }
        
        // Determine feedback level
        let feedbackLevel = 0;
        if (matchCount >= 6 || combo >= 4) feedbackLevel = 3;
        else if (matchCount >= 4 || combo >= 3) feedbackLevel = 2;
        else if (matchCount >= 3 || cascadeCount > 1) feedbackLevel = 1;
        
        // Sound based on feedback level
        if (feedbackLevel >= 3) {
            playSound('explosion');
            playSound('bigwin');
            showComboPopup('🔥 INCREDIBLE!', '#ff6b6b');
            screenShake(2);
        } else if (feedbackLevel >= 2) {
            playSound('combo');
            showComboPopup(cascadeCount > 1 ? '⚡ CASCADE!' : '✨ GREAT!', '#4ecdc4');
            screenShake(1);
        } else {
            playSound('match', 1 + (cascadeCount - 1) * 0.2);
        }
        
        // Process special gems that are being matched
        const specialExplosions = [];
        matchedPositions.forEach(pos => {
            const [row, col] = pos.split(',').map(Number);
            const gem = grid[row][col];
            
            if (gem.special === 'bomb') {
                // Explode 3x3 area
                for (let dr = -1; dr <= 1; dr++) {
                    for (let dc = -1; dc <= 1; dc++) {
                        const nr = row + dr;
                        const nc = col + dc;
                        if (nr >= 0 && nr < GRID_SIZE && nc >= 0 && nc < GRID_SIZE) {
                            matchedPositions.add(`${nr},${nc}`);
                        }
                    }
                }
                specialExplosions.push({ row, col, type: 'bomb' });
            } else if (gem.special === 'rainbow') {
                // Clear all gems of a random type
                const targetType = Math.floor(Math.random() * GEM_TYPES.length);
                for (let r = 0; r < GRID_SIZE; r++) {
                    for (let c = 0; c < GRID_SIZE; c++) {
                        if (grid[r][c].type === targetType) {
                            matchedPositions.add(`${r},${c}`);
                        }
                    }
                }
                specialExplosions.push({ row, col, type: 'rainbow' });
            }
        });
        
        // Visual effects for special explosions
        specialExplosions.forEach(exp => {
            const gems = document.querySelectorAll('.gem');
            const gem = gems[exp.row * GRID_SIZE + exp.col];
            if (gem) {
                const rect = gem.getBoundingClientRect();
                const boardRect = boardEl.getBoundingClientRect();
                const x = rect.left - boardRect.left + rect.width / 2;
                const y = rect.top - boardRect.top + rect.height / 2;
                
                createExplosion(x, y);
                playSound('explosion');
            }
        });
        
        // Remove matched gems with animation
        const gems = document.querySelectorAll('.gem');
        matchedPositions.forEach(pos => {
            const [row, col] = pos.split(',').map(Number);
            const index = row * GRID_SIZE + col;
            const gem = gems[index];
            
            if (gem) {
                const rect = gem.getBoundingClientRect();
                const boardRect = boardEl.getBoundingClientRect();
                
                gem.classList.add('matched');
                
                // Create particles
                const x = rect.left - boardRect.left + rect.width / 2;
                const y = rect.top - boardRect.top + rect.height / 2;
                const color = getComputedStyle(gem).background.match(/rgb\([^)]+\)/)?.[0] || '#fff';
                createParticles(x, y, color, feedbackLevel >= 2 ? 15 : 8);
                
                if (feedbackLevel >= 2) {
                    createScorePopup(x, y, Math.floor(totalPoints / matchCount), true);
                } else {
                    createScorePopup(x, y, Math.floor(totalPoints / matchCount));
                }
            }
            
            grid[row][col] = { type: -1, special: null };
        });
        
        // Update streak
        streak += cascadeCount;
        streakEl.textContent = streak;
        
        await delay(300);
        
        // Create special gems before dropping
        specialsToCreate.forEach(s => {
            if (grid[s.row][s.col].type === -1) {
                grid[s.row][s.col] = { type: s.type, special: s.special };
                playSound('powerup');
            }
        });
        
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
        allMatches = findMatches();
    }
    
    // Reset combo
    combo = 1;
    comboEl.textContent = 'x1';
    comboEl.classList.remove('combo-high');
    
    // Celebration for big cascades
    if (cascadeCount >= 4) {
        playSound('levelup');
        showComboPopup('🎰 MEGA CASCADE!', '#a855f7');
        createCoinBurst(window.innerWidth / 2, window.innerHeight / 2, 15);
        screenShake(2);
    } else if (cascadeCount >= 3) {
        playSound('bigwin');
        showComboPopup('💎 JACKPOT!', '#ffd93d');
        createCoinBurst(window.innerWidth / 2, window.innerHeight / 2, 10);
    }
}

// Drop gems
function dropGems() {
    for (let col = 0; col < GRID_SIZE; col++) {
        let emptyRow = GRID_SIZE - 1;
        
        for (let row = GRID_SIZE - 1; row >= 0; row--) {
            if (grid[row][col].type !== -1) {
                if (row !== emptyRow) {
                    grid[emptyRow][col] = grid[row][col];
                    grid[row][col] = { type: -1, special: null };
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
            if (grid[row][col].type === -1) {
                grid[row][col] = { 
                    type: Math.floor(Math.random() * GEM_TYPES.length),
                    special: null
                };
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
    
    // Keep special gems, shuffle regular ones
    const regularGems = [];
    const specialPositions = [];
    
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            if (grid[row][col].special) {
                specialPositions.push({ row, col, gem: grid[row][col] });
            } else {
                regularGems.push(grid[row][col]);
            }
        }
    }
    
    // Shuffle regular gems
    for (let i = regularGems.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [regularGems[i], regularGems[j]] = [regularGems[j], regularGems[i]];
    }
    
    // Put them back
    let gemIndex = 0;
    for (let row = 0; row < GRID_SIZE; row++) {
        for (let col = 0; col < GRID_SIZE; col++) {
            const isSpecial = specialPositions.find(p => p.row === row && p.col === col);
            if (!isSpecial) {
                grid[row][col] = regularGems[gemIndex++];
            }
        }
    }
    
    // Ensure no matches exist
    let matches = findMatches();
    let attempts = 0;
    while (matches.length > 0 && attempts < 100) {
        matches.forEach(m => {
            m.gems.forEach(({ row, col }) => {
                if (!grid[row][col].special) {
                    grid[row][col] = { 
                        type: Math.floor(Math.random() * GEM_TYPES.length),
                        special: null
                    };
                }
            });
        });
        matches = findMatches();
        attempts++;
    }
    
    renderGrid();
}

// Level complete
function levelComplete() {
    const lcScreen = document.getElementById('level-complete');
    const lcLevel = document.getElementById('lc-level');
    const lcScore = document.getElementById('lc-score');
    const lcStars = document.getElementById('lc-stars');
    
    if (lcScreen && lcLevel && lcScore && lcStars) {
        // Calculate stars
        const ratio = levelScore / levelGoal;
        let stars = '⭐';
        if (ratio >= 2) stars = '⭐⭐⭐';
        else if (ratio >= 1.5) stars = '⭐⭐';
        
        lcLevel.textContent = `LEVEL ${level}`;
        lcScore.textContent = levelScore.toLocaleString();
        lcStars.textContent = stars;
        
        lcScreen.classList.remove('hidden');
        playSound('levelup');
        
        // Celebration
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                createCoinBurst(
                    Math.random() * window.innerWidth,
                    Math.random() * window.innerHeight * 0.5,
                    5
                );
            }, i * 200);
        }
    }
}

// Next level
function nextLevel() {
    level++;
    const levelConfig = LEVELS[Math.min(level - 1, LEVELS.length - 1)];
    
    moves = levelConfig.moves;
    levelGoal = levelConfig.goal;
    levelScore = 0;
    streak = 0;
    combo = 1;
    
    if (levelEl) levelEl.textContent = `Level ${level}`;
    if (goalEl) goalEl.textContent = levelGoal.toLocaleString();
    movesEl.textContent = moves;
    streakEl.textContent = '0';
    comboEl.textContent = 'x1';
    updateProgress();
    
    const lcScreen = document.getElementById('level-complete');
    if (lcScreen) lcScreen.classList.add('hidden');
    
    initGrid();
    renderGrid();
    
    showComboPopup(`LEVEL ${level}`, '#4ecdc4');
    playSound('powerup');
}

// End game
function endGame() {
    finalScoreEl.textContent = score.toLocaleString();
    
    // Add stats
    const statsEl = document.getElementById('final-stats');
    if (statsEl) {
        statsEl.innerHTML = `
            <p>Level Reached: ${level}</p>
            <p>Total Matches: ${totalMatches}</p>
            <p>Best Streak: ${streak}</p>
        `;
    }
    
    gameOverScreen.classList.remove('hidden');
    playSound('bigwin');
    
    // Final celebration
    createCoinBurst(window.innerWidth / 2, window.innerHeight / 2, 20);
}

// Start game
function startGame() {
    level = 1;
    const levelConfig = LEVELS[0];
    
    score = 0;
    moves = levelConfig.moves;
    levelGoal = levelConfig.goal;
    levelScore = 0;
    combo = 1;
    streak = 0;
    totalMatches = 0;
    selectedGem = null;
    isProcessing = false;
    
    scoreEl.textContent = '0';
    movesEl.textContent = moves;
    comboEl.textContent = 'x1';
    streakEl.textContent = '0';
    if (levelEl) levelEl.textContent = 'Level 1';
    if (goalEl) goalEl.textContent = levelGoal.toLocaleString();
    updateProgress();
    
    initGrid();
    renderGrid();
    
    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    const lcScreen = document.getElementById('level-complete');
    if (lcScreen) lcScreen.classList.add('hidden');
    
    initAudio();
    playSound('powerup');
}

// Utility
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Event listeners
document.getElementById('start-btn')?.addEventListener('click', startGame);
document.getElementById('play-again')?.addEventListener('click', startGame);
document.getElementById('shuffle-btn')?.addEventListener('click', shuffleBoard);
document.getElementById('next-level-btn')?.addEventListener('click', nextLevel);

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

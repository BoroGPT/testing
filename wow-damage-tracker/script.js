// Player data storage
let players = [];

// Load players from localStorage on page load
window.addEventListener('DOMContentLoaded', () => {
    loadPlayers();
    renderPlayers();
});

// Save players to localStorage
function savePlayers() {
    localStorage.setItem('wowPlayers', JSON.stringify(players));
}

// Load players from localStorage
function loadPlayers() {
    const saved = localStorage.getItem('wowPlayers');
    if (saved) {
        players = JSON.parse(saved);
    }
}

// Add a new player
function addPlayer() {
    const nameInput = document.getElementById('playerName');
    const healthInput = document.getElementById('maxHealth');

    const name = nameInput.value.trim();
    const maxHealth = parseInt(healthInput.value);

    if (!name) {
        alert('Please enter a character name');
        return;
    }

    if (!maxHealth || maxHealth < 1) {
        alert('Please enter a valid max health');
        return;
    }

    const player = {
        id: Date.now(),
        name: name,
        maxHealth: maxHealth,
        currentHealth: maxHealth,
        isDead: false
    };

    players.push(player);
    savePlayers();
    renderPlayers();

    // Clear inputs
    nameInput.value = '';
    healthInput.value = '20';

    addToLog(`${name} joined the battle with ${maxHealth} HP!`);
}

// Remove a player
function removePlayer(id) {
    const player = players.find(p => p.id === id);
    if (player && confirm(`Remove ${player.name}?`)) {
        players = players.filter(p => p.id !== id);
        savePlayers();
        renderPlayers();
        addToLog(`${player.name} left the battle`);
    }
}

// Apply damage to a player
function applyDamage(id, amount) {
    const player = players.find(p => p.id === id);
    if (!player) return;

    if (amount < 0) {
        alert('Damage must be positive. Use Heal for healing.');
        return;
    }

    player.currentHealth = Math.max(0, player.currentHealth - amount);

    if (player.currentHealth === 0 && !player.isDead) {
        player.isDead = true;
        addToLog(`${player.name} has been defeated!`, 'death');
    }

    addToLog(`${player.name} took ${amount} damage (${player.currentHealth}/${player.maxHealth} HP remaining)`, 'damage');

    savePlayers();
    renderPlayers();
}

// Apply healing to a player
function applyHeal(id, amount) {
    const player = players.find(p => p.id === id);
    if (!player) return;

    if (amount < 0) {
        alert('Healing must be positive. Use Damage for dealing damage.');
        return;
    }

    const oldHealth = player.currentHealth;
    player.currentHealth = Math.min(player.maxHealth, player.currentHealth + amount);
    const actualHeal = player.currentHealth - oldHealth;

    if (player.isDead && player.currentHealth > 0) {
        player.isDead = false;
        addToLog(`${player.name} has been revived!`, 'heal');
    }

    if (actualHeal > 0) {
        addToLog(`${player.name} healed for ${actualHeal} HP (${player.currentHealth}/${player.maxHealth} HP)`, 'heal');
    }

    savePlayers();
    renderPlayers();
}

// Reset a single player's health
function resetPlayer(id) {
    const player = players.find(p => p.id === id);
    if (!player) return;

    player.currentHealth = player.maxHealth;
    player.isDead = false;

    addToLog(`${player.name} restored to full health!`, 'heal');

    savePlayers();
    renderPlayers();
}

// Reset all players
function resetAll() {
    if (players.length === 0) return;

    if (confirm('Reset all characters to full health?')) {
        players.forEach(player => {
            player.currentHealth = player.maxHealth;
            player.isDead = false;
        });

        savePlayers();
        renderPlayers();
        addToLog('All characters restored to full health!', 'heal');
    }
}

// Clear all players
function clearAll() {
    if (players.length === 0) return;

    if (confirm('Remove all characters? This cannot be undone!')) {
        players = [];
        savePlayers();
        renderPlayers();
        addToLog('All characters removed from battle');
    }
}

// Add entry to combat log
function addToLog(message, type = 'info') {
    const log = document.getElementById('combatLog');
    const timestamp = new Date().toLocaleTimeString();
    const entry = document.createElement('div');
    entry.className = `log-entry log-${type}`;
    entry.textContent = `[${timestamp}] ${message}`;
    log.insertBefore(entry, log.firstChild);

    // Limit log to 50 entries
    while (log.children.length > 50) {
        log.removeChild(log.lastChild);
    }
}

// Clear combat log
function clearLog() {
    const log = document.getElementById('combatLog');
    log.innerHTML = '';
}

// Get health bar color class
function getHealthColorClass(currentHealth, maxHealth) {
    const percentage = (currentHealth / maxHealth) * 100;
    if (percentage <= 25) return 'critical';
    if (percentage <= 50) return 'low';
    return '';
}

// Render all players
function renderPlayers() {
    const container = document.getElementById('playersContainer');

    if (players.length === 0) {
        container.innerHTML = '<p style="text-align: center; padding: 40px; opacity: 0.7;">No characters yet. Add one to get started!</p>';
        return;
    }

    container.innerHTML = players.map(player => {
        const healthPercentage = (player.currentHealth / player.maxHealth) * 100;
        const colorClass = getHealthColorClass(player.currentHealth, player.maxHealth);
        const deadClass = player.isDead ? 'dead' : '';

        return `
            <div class="player-card ${deadClass}">
                <div class="player-header">
                    <span class="player-name">
                        ${player.name}
                        ${player.isDead ? '<span class="dead-indicator">DEFEATED</span>' : ''}
                    </span>
                    <button class="remove-btn" onclick="removePlayer(${player.id})">Remove</button>
                </div>

                <div class="health-bar-container">
                    <div class="health-info">
                        <span>Health</span>
                        <span>${player.currentHealth} / ${player.maxHealth}</span>
                    </div>
                    <div class="health-bar">
                        <div class="health-fill ${colorClass}" style="width: ${healthPercentage}%">
                            ${healthPercentage.toFixed(0)}%
                        </div>
                    </div>
                </div>

                <div class="damage-controls">
                    <input type="number"
                           class="damage-input"
                           id="damage-${player.id}"
                           placeholder="Enter amount"
                           value="1"
                           min="0">
                    <button class="damage-btn" onclick="applyDamage(${player.id}, parseInt(document.getElementById('damage-${player.id}').value) || 0)">
                        Deal Damage
                    </button>
                    <button class="heal-btn" onclick="applyHeal(${player.id}, parseInt(document.getElementById('damage-${player.id}').value) || 0)">
                        Heal
                    </button>
                </div>

                <div class="quick-damage">
                    <button class="quick-btn" onclick="applyDamage(${player.id}, 1)">-1</button>
                    <button class="quick-btn" onclick="applyDamage(${player.id}, 2)">-2</button>
                    <button class="quick-btn" onclick="applyDamage(${player.id}, 5)">-5</button>
                    <button class="quick-btn" onclick="applyDamage(${player.id}, 10)">-10</button>
                </div>

                <button class="reset-btn" onclick="resetPlayer(${player.id})">Reset to Full Health</button>
            </div>
        `;
    }).join('');
}

// Allow Enter key to add player
document.addEventListener('DOMContentLoaded', () => {
    const nameInput = document.getElementById('playerName');
    const healthInput = document.getElementById('maxHealth');

    [nameInput, healthInput].forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                addPlayer();
            }
        });
    });
});

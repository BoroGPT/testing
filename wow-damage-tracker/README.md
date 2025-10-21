# World of Warcraft Boardgame Damage Tracker

A web-based damage tracking application for the World of Warcraft board game. Track player health, damage, and healing in real-time with a clean, intuitive interface.

## Features

- **Player Management**: Add and remove characters with custom names and max health
- **Damage Tracking**: Deal damage to characters with custom amounts or quick buttons
- **Healing System**: Heal characters back to health
- **Health Visualization**: Visual health bars with color-coded status (green/yellow/red)
- **Combat Log**: Real-time log of all damage, healing, and game events
- **Persistent Storage**: Player data is saved automatically to browser localStorage
- **Quick Damage Buttons**: Fast damage application with -1, -2, -5, and -10 buttons
- **Status Indicators**: Clear visual feedback for defeated characters
- **Reset Options**: Reset individual characters or all at once

## How to Use

### Getting Started

1. Open `index.html` in your web browser
2. The app will automatically load any previously saved characters

### Adding Characters

1. Enter a character name in the "Character Name" field
2. Set the max health (default is 20)
3. Click "Add Character" or press Enter

### Tracking Damage

**Custom Amount:**
- Enter an amount in the character's input field
- Click "Deal Damage" to apply

**Quick Damage:**
- Use the quick buttons (-1, -2, -5, -10) for fast damage application

### Healing

1. Enter the healing amount in the character's input field
2. Click "Heal" to restore health

### Managing Characters

- **Reset Single Character**: Click "Reset to Full Health" on any character card
- **Reset All**: Click "Reset All" to restore all characters to full health
- **Remove Character**: Click "Remove" on any character card
- **Clear All**: Click "Clear All Characters" to remove everyone

### Combat Log

- View all game events in chronological order (newest first)
- Color-coded entries:
  - Red: Damage dealt
  - Green: Healing applied
  - Bold Red: Character defeated
- Click "Clear Log" to reset the combat log

## Features Explained

### Health Bar Colors

- **Green**: Above 50% health
- **Yellow**: 26-50% health
- **Red**: 0-25% health (critical)

### Character States

- **Active**: Normal appearance, ready for battle
- **Defeated**: Red background, "DEFEATED" indicator shown
- **Revived**: Automatically cleared when healed above 0 HP

### Data Persistence

All character data is automatically saved to your browser's localStorage. Your game state persists between sessions.

## Browser Compatibility

Works on all modern browsers:
- Chrome/Edge
- Firefox
- Safari
- Opera

## Tips

- Use quick damage buttons for common attack values
- The combat log helps track game history
- Health bars provide at-a-glance status of all characters
- Characters are saved automatically - no need to manually save

## Technical Details

Built with:
- HTML5
- CSS3 (with modern gradients and backdrop-filter effects)
- Vanilla JavaScript (no frameworks required)
- localStorage for data persistence

## License

Free to use for World of Warcraft board game sessions.

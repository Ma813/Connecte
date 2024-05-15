import React, { useState } from 'react';

export default function About() {
    const [content, setContent] = useState('gameRules');

    const creatorsContent = (
        <div>
            <h2>Authors:</h2>
            <div style={{  marginBottom: '10px' }}>
                <img src="https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png" alt="Martynas Mačiulaitis" style={{ width: '50px', height: '50px', marginRight: '10px' }} />
                <p>Martynas Mačiulaitis</p>
            </div>
            <div style={{  marginBottom: '10px' }}>
                <img src="https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png" alt="Martynas Jukna" style={{ width: '50px', height: '50px', marginRight: '10px' }} />
                <p>Martynas Jukna</p>
            </div>
            <div style={{  marginBottom: '10px' }}>
                <img src="https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png" alt="Dominykas Pranaitis" style={{ width: '50px', height: '50px', marginRight: '10px' }} />
                <p>Dominykas Pranaitis</p>
            </div>
            <div style={{  marginBottom: '10px' }}>
                <img src="https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png" alt="Ainis Vaičiūnas" style={{ width: '50px', height: '50px', marginRight: '10px' }} />
                <p>Ainis Vaičiūnas</p>
            </div>
            <div style={{  marginBottom: '10px' }}>
                <img src="https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png" alt="Julius Barauskas" style={{ width: '50px', height: '50px', marginRight: '10px' }} />
                <p>Julius Barauskas</p>
            </div>
            <div style={{  marginBottom: '10px' }}>
                <img src="https://cdn.pixabay.com/photo/2018/11/13/21/43/avatar-3814049_1280.png" alt="Matas Gudliauskas" style={{ width: '50px', height: '50px', marginRight: '10px' }} />
                <p>Matas Gudliauskas</p>
            </div>
        </div>
    );
    

    const faqContent = (
        <div>
            <h2>FAQ</h2>
            <p><strong>1. How do you start a new game in Connectė?</strong></p>
            <p>You can start a new game by clicking on the "Create room" button. This allows you to set up a game room that others can join.</p>
            
            <p><strong>2. Can I join a game if I don’t know anyone?</strong></p>
            <p>No, public rooms feature is not available yet.</p>
    
            <p><strong>3. What is the goal of Connect4?</strong></p>
            <p>The goal is to connect four of your discs in a row either horizontally, vertically, or diagonally before your opponent does.</p>
    
            <p><strong>4. Are there different game modes available?</strong></p>
            <p>Yes, in addition to the standard game, there are modes like Memory Game, Bot Game, and custom games where you can adjust the height and length of the board.</p>
    
            <p><strong>5. What is a Memory Game mode?</strong></p>
            <p>In Memory Game mode, each disc's color is hidden after being placed, requiring players to remember the position and color of each disc.</p>
    
            <p><strong>6. Can I play against the computer?</strong></p>
            <p>Yes, the Bot Game mode allows you to play against a computer controlled opponent that uses algorithms to decide moves.</p>
    
            <p><strong>7. How can I change the number of players in a game?</strong></p>
            <p>When creating a room, you can select the number of players you want in the game.</p>
    
            <p><strong>8. What does the "Number of circles to connect to win" setting do?</strong></p>
            <p>This setting allows you to change the traditional requirement from four connected discs to another number, altering the game’s difficulty and duration.</p>
    
            <p><strong>9. Is there a way to practice before playing with others?</strong></p>
            <p>Yes, you can practice playing against computer. Also you should keep in mind that all games are saved to your game history.</p>
    
            <p><strong>10. What happens if the board fills up before anyone connects four?</strong></p>
            <p>If the board fills up and no player has connected the required number of discs, the game ends in a draw.</p>
        </div>
    );
    

    const gameRulesContent = (
        <div>
            <h2>Game Rules</h2>
            <p>Connect4 is played by two players who take turns dropping colored discs into a vertically suspended grid. The objective is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.</p>
            <p><strong>Create room:</strong> Starts a new game room where other players can join. Only the creator can set game parameters.</p>
            <p><strong>Input room ID:</strong> Enter the ID of an existing game room you wish to join. This ID is provided by the game room creator.</p>
            <p><strong>Join game room:</strong> After entering a valid room ID, this button connects you to the specified game room.</p>
            <h3>Game Options</h3>
            <p><strong>Standard game:</strong> Play the classic version of Connect4 without any modifications.</p>
            <p><strong>Number of players:</strong> Select how many players will be in the game.</p>
            <p><strong>Memory Game:</strong> In this mode, each player must remember the colors of discs that are hidden after being placed.</p>
            <p><strong>Bot Game:</strong> Play against a computer-controlled opponent.</p>
            <p><strong>Height of the board:</strong> Adjusts the number of rows in the game board.</p>
            <p><strong>Length of the board:</strong> Adjusts the number of columns in the game board.</p>
            <p><strong>Number of circles to connect to win:</strong> Change the traditional game rule from four connected discs to another number.</p>
        </div>
    );
    
    

    const renderContent = () => {
        switch (content) {
            case 'faq':
                return faqContent;
            case 'gameRules':
                return gameRulesContent;
            case 'creators':
            default:
                return creatorsContent;
        }
    };

    return (
        <div>
            <h1>Connectė</h1>
            <p>Connectė is an implementation of the game Connect4 using React and Python flask. In the game, you can play against other opponents or a bot that utilizes the alpha-beta pruning algorithm to select the moves that lead to the best outcome. The website also implements multiple game modes that would be impossible to play on a physical board.</p>
            
            <button style={{ marginRight: '10px' }} className="btn btn-secondary" onClick={() => setContent('gameRules')}>Game Rules</button>

            <button style={{ marginRight: '10px' }} className="btn btn-secondary" onClick={() => setContent('faq')}>FAQ</button>

            <button style={{ marginRight: '10px' }} className="btn btn-secondary" onClick={() => setContent('creators')}>Creators</button>
            {renderContent()}
        </div>
    );
}

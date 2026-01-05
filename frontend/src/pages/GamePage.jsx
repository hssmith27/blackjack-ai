import { useState, useEffect } from 'react'
import Card from '../components/Card.jsx'
import '../pages_styles/GamePage.css'

function GamePage() {
    // Track accuracy
    const [handsPlayed, setHandsPlayed] = useState(0)
    const [handsCorrect, setHandsCorrect] = useState(0)

    // Store player and dealer cards
    const [playerCards, setPlayerCards] = useState([])
    const [dealerCard, setDealerCard] = useState("")

    // Hand Info
    const [trueCount, setTrueCount] = useState(0)

    // AI Policy
    const [modelPolicy, setModelPolicy] = useState("")

    // Deck management
    const [deckID, setDeckID] = useState("")
    const [numCards, setNumCards] = useState(0)

    // Load shoe when loading the page
    useEffect(() => {
        loadShoe();
    }, [])

    // Loads in the shoe from an API
    async function loadShoe() {
        const response = await fetch('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6');
        const data = await response.json();
        setDeckID(data['deck_id']);
        setNumCards(data['remaining']);
    }

    // Reset shoe
    async function resetShoe() {
        const response = await fetch('https://deckofcardsapi.com/api/deck/' + deckID + '/shuffle/');
        const data = await response.json();
        setNumCards(data['remaining']);
    }

    // Deal cards to player and dealer
    async function dealCards() {
        const response = await fetch('https://deckofcardsapi.com/api/deck/' + deckID + '/draw/?count=3');
        const data = await response.json();
        setNumCards(data['remaining']);

        // Set cards
        const cards = data['cards'].map(card => card.code);
        setPlayerCards(cards.slice(0, 2))
        setDealerCard(cards[2])

        // Reset shoe if less than a deck remaining
        if (data['remaining'] < 52) {
            resetShoe();
        }
        
        // Set a random True Count between -5 and 5
        setTrueCount(Math.floor(Math.random() * (11)) -5)
    }

    // Fetches the optimal policy from the backend
    async function fetchOptimal() {
        const response = await fetch('http://127.0.0.1:5000/get_policy', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({player_cards: playerCards, dealer_card: dealerCard, true_count: trueCount})
        });
        const data = await response.json();
        setModelPolicy(data['policy']);
    }

    return (
        <div className="game-page">
            <div className="top-bar">
                <h1>{handsPlayed} / {handsCorrect}</h1>
            </div>
            <div className="game">
                <div className="board">
                    <div className="cards dealer-card">
                        {dealerCard && <Card card={dealerCard} />}
                    </div>
                    <div className="cards player-cards">
                        {playerCards.map((card) => (
                            <Card card={card} />    
                        ))}
                    </div>
                </div>
    
                <div className="game-actions" >
                    <button onClick={dealCards}>Hit</button>
                    <button onClick={fetchOptimal}>Stand</button>
                    <button>Double Down</button>
                    <button>Split</button>
                    <p>{trueCount}</p>
                </div>
            </div>
        </div>
    );
}

export default GamePage
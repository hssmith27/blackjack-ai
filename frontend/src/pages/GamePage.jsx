import { useState } from 'react'
import Card from '../components/Card.jsx'
import '../pages_styles/GamePage.css'

function GamePage() {
    // Track accuracy
    const [handsPlayed, setHandsPlayed] = useState(0)
    const [handsCorrect, setHandsCorrect] = useState(0)

    // Store player and dealer cards
    const [playerCards, setPlayerCards] = useState(["AH", "0C"])
    const [dealerCard, setDealerCard] = useState("AS")

    // Hand Info
    const [trueCount, setTrueCount] = useState(1)

    // AI Policy
    const [modelPolicy, setModelPolicy] = useState("")

    // Fetches the optimal policy from the backend
    async function fetchOptimal() {
        const response = await fetch('http://127.0.0.1:5000/get_policy', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({player_cards: playerCards, dealer_card: dealerCard, true_count: trueCount})
        });
        const data = await response.json();
        setModelPolicy(data['policy'])
    }

    return (
        <div className="game-page">
            <div className="top-bar">
                <h1>{handsPlayed} / {handsCorrect}</h1>
            </div>
            <div className="game">
                <div className="cards dealer-card">
                    {dealerCard && <Card card={dealerCard} />}
                </div>
                <div className="cards player-cards">
                    {playerCards.map((card) => (
                        <Card card={card} />    
                    ))}
                </div>
                <div className="game-actions" >
                    <button onClick={fetchOptimal}>{modelPolicy}</button>
                </div>
            </div>
        </div>
    )
}

export default GamePage
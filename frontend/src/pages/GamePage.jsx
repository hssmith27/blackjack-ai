import { useState } from 'react'
import Card from '../components/Card.jsx'
import '../pages_styles/GamePage.css'

function GamePage() {
    const [playerCards, setPlayerCards] = useState(["KH", "0C"])
    const [dealerCards, setDealerCards] = useState(["AS"])
    const [handsPlayed, setHandsPlayed] = useState(0)
    const [handsCorrect, setHandsCorrect] = useState(0)

    return (
        <div className="game-page">
            <div className="top-bar">
                <h1>{handsPlayed} / {handsCorrect}</h1>
            </div>
            <div className="game">
                <div className="cards dealer-cards">
                    {dealerCards.map((card) => (
                        <Card card={card} />    
                    ))}
                </div>
                <div className="cards player-cards">
                    {playerCards.map((card) => (
                        <Card card={card} />    
                    ))}
                </div>
                <div className="game-actions">

                </div>
            </div>
        </div>
    )
}

export default GamePage
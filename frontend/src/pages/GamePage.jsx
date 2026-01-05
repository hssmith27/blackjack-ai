import { useState } from 'react'
import '../pages_styles/GamePage.css'

function GamePage() {
    const [playerCards, setPlayerCards] = useState([])
    const [dealerCard, setDealerCard] = useState('')
    const [handsPlayed, setHandsPlayed] = useState(0)
    const [handsCorrect, setHandsCorrect] = useState(0)

    return (
        <div class="game-page">
            <div class="top-bar">
                <h1>{handsPlayed} / {handsCorrect}</h1>
            </div>
            <div class="game">

            </div>
        </div>
    )
}

export default GamePage
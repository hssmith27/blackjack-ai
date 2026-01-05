import { useState } from 'react'
import '../components_styles/Card.css'

function Card( {card} ) {
    const rankVal = card.slice(0, -1);
    const rank = rankVal === "0" ? "10" : rankVal
    const suitSymbol = { S: "♠", H: "♥", D: "♦", C: "♣" };
    const suitLetter = card.slice(-1);
    const suit = suitSymbol[suitLetter]
    const isRed = suitLetter === "H" || suitLetter === "D";
    const color = isRed ? "red" : "black"

    return (
        <div className={`card ${color}`}>
            <div className="top">{rank}{suit}</div>
            <div className="bottom">{rank}{suit}</div>
        </div>
    )
}

export default Card
import { useState, useEffect } from 'react'
import Card from '../components/Card.jsx'
import '../pages_styles/GamePage.css'
import blackjackLogo from "../assets/blackjack_logo.png"

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

    // Handle actions
    const [buttonColors, setButtonColors] = useState({})
    const [actionsAvailable, setActionsAvailable] = useState(false)

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

    // Deals cards and resets states
    async function playHand() {
        dealCards()
        setModelPolicy("")
        setActionsAvailable(true)
        setButtonColors({})
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
        return data['policy'];
    }

    // Handle game actions
    async function handleGameAction(buttonId) {
        const policy = await fetchOptimal();
        setActionsAvailable(false);
        setHandsPlayed(prev => prev + 1);
        
        // Set correct answer to green
        setButtonColors((prev) => ({...prev, [policy]: "green"}));

        // If wrong, set wrong answer to red
        if (policy != buttonId) {
            setButtonColors((prev) => ({...prev, [buttonId]: "red"}));
        }
        // Update the number of correct decisions
        else {
            setHandsCorrect(prev => prev + 1);
        }
    }

    return (
        <div className="game-page">
            <div className="top-bar">
                <img className="logo" src={blackjackLogo}/>
                <h1>{handsCorrect}/{handsPlayed} </h1>
            </div>
            <div className="game">
                <div className="board">
                    <div className="game-header">
                        {!actionsAvailable && <button onClick={playHand}>Deal Cards</button>}
                        <h2>True Count: {trueCount}</h2>
                    </div>
                    <hr />
                    <div className="cards dealer-card">
                        {dealerCard && <Card card={dealerCard} />}
                        {!dealerCard && <Card card={"AS"} hidden={true} />}
                    </div>
                    <hr />
                    <div className="cards player-cards">
                        {playerCards.map((card) => (
                            <Card card={card} />    
                        ))}
                        {playerCards.length === 0 && <Card card={"AS"} hidden={true} />}
                    </div>
                </div>
    
                <div className="game-actions" >
                    <button disabled={!actionsAvailable} className={buttonColors.hit} onClick={() => handleGameAction("hit")}>Hit</button>
                    <button disabled={!actionsAvailable} className={buttonColors.stand} onClick={() => handleGameAction("stand")}>Stand</button>
                    <button disabled={!actionsAvailable} className={buttonColors.double} onClick={() => handleGameAction("double")}>Double Down</button>
                    <button disabled={!actionsAvailable} className={buttonColors.split} onClick={() => handleGameAction("split")}>Split</button>
                </div>
            </div>
        </div>
    );
}

export default GamePage
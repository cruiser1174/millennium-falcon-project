import React from "react";
import { Route } from "./Route";

export function Odds(props) {
    
    return (
        <div className="odds-section">
            <h2 id="odds-title" className='jedi-title'>odds of success</h2>
            <img id="odds-gif" src={props.image} alt="odds-gif"/>
            {props.odds === 0 ? 
                <h3 id="odds-statement">There's a {props.odds}% chance of success</h3> :
                <div className="successful-odds">
                    <h3 id="odds-statement">There's a {props.odds}% chance of success using the following route:</h3>
                    <Route route={props.route} />
                </div>
            }
        </div>
        
    );
}
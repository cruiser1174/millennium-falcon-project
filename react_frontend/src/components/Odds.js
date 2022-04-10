import React from "react";
import { Route } from "./Route";

export function Odds(props) {
    
    return (
        <div className="odds-section">
            <img src={props.image}/>
            {props.odds === 0 ? 
                <h4>There's a {props.odds}% chance of success</h4> :
                <div className="successful-odds">
                    <h4>There's a {props.odds}% chance of success follwing this route:</h4>
                    <Route route={props.route} />
                </div>
            }
        </div>
        
    );
}
import React from "react";

export function Route(props) {
    return (
        <div>
            <p> Route: </p>
            {props.route.map(stop => (
                <table>
                    <tbody>
                    <tr>
                        <td>Day {stop.arrival_day}:</td>
                        {stop.arrival_day === 0 ? 
                        <td>Start at {stop.planet}.</td> :
                        <td>Arrive at {stop.planet}.</td>
                        }
                        {stop.refueled && <td>Stay a day to refuel.</td>}
                        {stop.waited_for_hunters && <td>Wait for bounty hunters to leave next planet.</td>}
                    </tr>
                    {stop.departure_day && 
                        <tr>
                        <td>Day {stop.departure_day}:</td>
                        <td>Depart {stop.planet}.</td>
                        </tr>
                    }
                    </tbody>
                </table>
                ))}
        </div>
    );
}
import React from "react";

export function Route(props) {
    return (
        <table id="route-table">
            <tbody>
                {props.route.map((stop, index, stops) => (
                    <div id={stop.planet} className="stop-details">
                        <div className="arrival-container">
                            <tr className="stop-arrival">
                                <td id={"day-arrival-row-"+stop.arrival_day} className="day-arrival-row"><text className="route-text">Day {stop.arrival_day}:</text></td>
                                <td>
                                    <text className="route-row-data">
                                        {stop.arrival_day === 0 ? 
                                            <text id="start-planet" className="route-text">Start at {stop.planet}. </text> :
                                            <text id="arrival-planet" className="route-text">Arrive at {stop.planet}. </text>}
                                            
                                        {stop.departure_day === stop.arrival_day && 
                                            <text id="quick-leave" className="route-text">Leave right away for {stops[index + 1].planet}. </text>}

                                        {stop.refueled && 
                                            <text id="refuel" className="route-text">Stay a day to refuel. </text>}

                                        {stop.hunter_count > 0 && (stop.hunter_count > 1 ? 
                                            <text id="hide" className="route-text">{stop.hunter_count} days spent hiding in presence of bounty hunters. </text> :
                                            <text id="hide" className="route-text">{stop.hunter_count} day spent hiding in presence of bouty hunters. </text>)}

                                        {stop.waited_for_hunters > 0 && (stop.waited_for_hunters > 1 ? 
                                            <text id="wait" className="route-text">Wait {stop.waited_for_hunters} days for bounty hunters to leave {stops[index + 1].planet}. </text> :
                                            <text id="wait" className="route-text">Wait {stop.waited_for_hunters} day for bounty hunters to leave {stops[index + 1].planet}. </text>)}
                                    </text>
                                </td>
                            </tr>
                        </div>                            

                        {!isNaN(stop.departure_day) && stop.departure_day !== stop.arrival_day &&
                            <div className="departure-container">
                                <tr className="stop-departure">
                                    <td id={"day-arrival-row-"+stop.arrival_day} className="day-arrival-row"><text className="route-text">Day {stop.departure_day}:</text></td>
                                    <td className="route-row-data"><text className="route-text">Depart {stop.planet} for {stops[index + 1].planet}.</text></td>
                                </tr>
                            </div>}
                    </div>
                ))}
            </tbody>
        </table>
    );
}
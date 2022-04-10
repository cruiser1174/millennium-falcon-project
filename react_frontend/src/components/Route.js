import React from "react";

export function Route(props) {
    return (
        <table id="route-table">
            <tbody>
                {props.route.map((stop, index, stops) => (
                    <div id={stop.planet} className="stop-details">
                        <div className="arrival-container">
                            <tr className="stop-arrival">
                                <td className="day"><h4>Day {stop.arrival_day}:</h4></td>

                                {stop.arrival_day === 0 ? 
                                <td className="start-planet"><h4>Start at {stop.planet}.</h4></td> :
                                <td className="arrival-planet"><h4>Arrive at {stop.planet}.</h4></td>}

                                {stop.departure_day === stop.arrival_day && <td className="quick-leave"><h4>Leave right away for {stops[index + 1].planet}.</h4></td>}

                                {stop.refueled && <td className="refuel"><h4>Stay a day to refuel.</h4></td>}
                                
                                {stop.hunter_count > 0 && (stop.hunter_count > 1 ? 
                                    <td className="hide"><h4>{stop.hunter_count} days spent hiding in presence of bounty hunters.</h4></td> :
                                    <td className="hide"><h4>{stop.hunter_count} day spent hiding in presence of bouty hunters.</h4></td>)}

                                {stop.waited_for_hunters > 0 && (stop.waited_for_hunters > 1 ? 
                                    <td className="wait"><h4>Wait {stop.waited_for_hunters} days for bounty hunters to leave {stops[index + 1].planet}.</h4></td> :
                                    <td className="wait"><h4>Wait {stop.waited_for_hunters} day for bounty hunters to leave {stops[index + 1].planet}.</h4></td>)}
                            </tr>
                        </div>                            

                        {!isNaN(stop.departure_day) && stop.departure_day !== stop.arrival_day &&
                            <div className="departure-container">
                                <tr className="stop-departure">
                                    <td className="day"><h4>Day {stop.departure_day}:</h4></td>
                                    <td className="departure-planet"><h4>Depart {stop.planet} for {stops[index + 1].planet}.</h4></td>
                                </tr>
                            </div>}
                    </div>
                ))}
            </tbody>
        </table>
    );
}
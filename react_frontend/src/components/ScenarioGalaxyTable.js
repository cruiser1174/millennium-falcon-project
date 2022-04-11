import React from "react";

export function ScenarioGalaxyTable(props) {
    return (
        <table id="scenario-comparison-table" className="scenario-galaxy-table">
            <colgroup>
                <col id="planets-col" />
                <col id="neighbors-col" />
                <col id="hunters-col" />
            </colgroup>

            <thead>
                <tr>
                    <th id="planets-header" className="table-header">Planets</th>
                    <th id="neighbors-header" className="table-header">Neighbors</th>
                    <th id="hunters-header" className="table-header">Days with bounty hunters</th>
                </tr>
            </thead>

            <tbody>
            {props.planets.map(planet => (
                <tr>
                    <td id={planet} className="planet">{planet}</td>
                    <td id={planet+"-neighbors"} className="neighbor">
                        {Object.keys(props.neighbors[planet]).map(neighbor => (
                            props.neighbors[planet][neighbor] > 1 ? 
                                <p id={neighbor} className="neighbor">{neighbor} ({props.neighbors[planet][neighbor]} days)</p> :
                                <p id={neighbor} className="neighbor">{neighbor} ({props.neighbors[planet][neighbor]} day)</p>
                        ))}
                    </td>
                    <td id={planet+"-hunter-days"} className="hunter-days">{props.scenarioDays[planet]}</td>
                </tr>
            ))}
            </tbody>
        </table>
    );
}
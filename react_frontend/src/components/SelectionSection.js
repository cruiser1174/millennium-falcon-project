/** @jsxImportSource @emotion/react */
import React from "react";
import { Dropdown } from "./Dropdown";
import { SubmitScenarioForm } from './SubmitScenarioForm';

export function SelectionSection(props) {
    return(
        <div className="section-1">
            <h1 id="app-title" className='jedi-title'>Kessel Run odds calculator</h1>
            <div className="selection-section">
                <div className="dropdown-container">
                    <h3>Select a galaxy and scenario</h3>
                    <div className="dropdown-box">
                        <Dropdown id="galaxy" items={props.galaxies} onChange={props.updateSelectedGalaxy} />
                        <Dropdown id="scenario" items={props.scenarios} onChange={props.updateSelectedScenario} />
                    </div>
                </div>
                <div className="upload">
                    <SubmitScenarioForm handleSubmit={props.handleSubmit} handleUpload={props.handleUpload} file={props.file}/>
                </div>
            </div>
        </div>
    );
}
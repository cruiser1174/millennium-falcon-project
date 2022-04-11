/** @jsxImportSource @emotion/react */
import React from "react";
import { Dropdown } from "./Dropdown";
import { SubmitScenarioForm } from './SubmitScenarioForm';

export function SelectionSection(props) {
    const selectionStyle = {
        display: 'flex',
        flexFlow: 'row wrap',
        width: '100%',
        justifyContent: 'space-around',
        alignContent: 'flex-start',
        marginBottom: '2rem'

    }

    const dropdownBoxStyle = {
        display: 'flex',
        flexDirection: 'column',
        margin: '0.5rem 4rem'
    }

    const dropdownStyle = {
        display: 'flex',
        justifyContent: 'space-around'
    }

    return(
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
    );
}
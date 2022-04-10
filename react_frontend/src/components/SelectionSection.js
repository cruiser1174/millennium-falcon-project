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

    const uploadStyle = {}
    return(
        <div className="selectionSection" css={selectionStyle}>
            <div className="dropdownBox" css={dropdownBoxStyle}>
                <h3>Select a galaxy and scenario</h3>
                <div className="dropdowns" css={dropdownStyle}>
                    <Dropdown id="galaxy" items={props.galaxies} onChange={props.updateSelectedGalaxy} />
                    <Dropdown id="scenario" items={props.scenarios} onChange={props.updateSelectedScenario} />
                </div>
            </div>
            <div className="upload" css={uploadStyle}>
                <SubmitScenarioForm onSubmit={props.handleSubmit} handleUpload={props.handleUpload}/>
            </div>
        </div>
    );
}
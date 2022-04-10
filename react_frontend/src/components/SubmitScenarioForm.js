/** @jsxImportSource @emotion/react */
import React from "react";

export function SubmitScenarioForm(props) {
    
    return (
        <div css={{margin: '0.5rem 4rem'}}>
            <h3>Upload a new scenario</h3>
            <form onSubmit={props.handleSubmit}>
                <input type="file" onChange={props.handleUpload}/>
                <button type="submit">Upload</button>
            </form>
        </div>
    );
}
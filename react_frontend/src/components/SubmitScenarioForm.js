import React from "react";

export function SubmitScenarioForm(props) {
    
    return (
        <div>
            <p>Upload a new scenario</p>
            <form onSubmit={props.handleSubmit}>
                <input type="file" onChange={props.handleUpload}/>
                <button type="submit">Upload</button>
            </form>
        </div>
    );
}
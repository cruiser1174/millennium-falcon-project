import React from "react";

export function Dropdown(props) {
    function handleChange(event) {
        const newValue = event.target.value;
        props.onChange(newValue);
    }

    return (
        <div>
            <select className="dropdown" id={props.id + "-dropdown"} onChange={handleChange}>
                <option selected disabled hidden>Select {props.id}</option>
                {props.items.map(item => (
                    <option value={item}>{item}</option>
                ))}
            </select>
        </div>
    );
}
import React from "react";

export function Dropdown(props) {
    function handleChange(event) {
        const newValue = event.target.value;
        props.onChange(newValue);
    }

    return (
        <select name="selectList" id="selectList" onChange={handleChange}>
            {props.items.map(item => (
                <option value={item}>{item}</option>
            ))}
        </select>
    );
}
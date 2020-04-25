import React, { Component } from "react";
import $ from "jquery";

import "../stylesheets/FormView.css";

class FormView extends Component {
    constructor(props) {
        super();
        this.state = {
            question: "",
            answer: "",
            difficulty: 1,
            category: 1,
            categories: {},
        };
    }

    componentDidMount() {
        $.ajax({
            url: `/categories`,
            type: "GET",
            success: result => {
                this.setState({ categories: result.categories });
            },
            error: error => {
                alert(
                    "Unable to load categories. Please try your request again",
                );
            },
        });
    }

    submitQuestion = event => {
        event.preventDefault();
        $.ajax({
            url: "/questions",
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({
                question: this.state.question,
                answer: this.state.answer,
                difficulty: this.state.difficulty,
                category: this.state.category,
            }),
            xhrFields: {
                withCredentials: true,
            },
            crossDomain: true,
            success: result => {
                document.getElementById("add-question-form").reset();
                document
                    .querySelector("#success-well")
                    .classList.toggle("hidden");

                setTimeout(
                    () =>
                        document
                            .querySelector("#success-well")
                            .classList.toggle("hidden"),
                    2000,
                );
            },
            error: error => {
                document
                    .querySelector("#failure-well")
                    .classList.toggle("hidden");

                setTimeout(
                    () =>
                        document
                            .querySelector("#failure-well")
                            .classList.toggle("hidden"),
                    2000,
                );
            },
        });
    };

    handleChange = event => {
        this.setState({ [event.target.name]: event.target.value });
    };

    render() {
        return (
            <div id="add-form">
                <h2>Add a New Trivia Question</h2>
                <form
                    className="form-view"
                    id="add-question-form"
                    onSubmit={this.submitQuestion}>
                    <label>
                        Question
                        <input
                            type="text"
                            name="question"
                            onChange={this.handleChange}
                            required
                        />
                    </label>
                    <label>
                        Answer
                        <input
                            type="text"
                            name="answer"
                            onChange={this.handleChange}
                            required
                        />
                    </label>
                    <label>
                        Difficulty
                        <select
                            name="difficulty"
                            onChange={this.handleChange}
                            required>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </label>
                    <label>
                        Category
                        <select
                            name="category"
                            onChange={this.handleChange}
                            required>
                            {Object.keys(this.state.categories).map(
                                id => {
                                    return (
                                        <option key={id} value={id}>
                                            {
                                                this.state.categories[
                                                    id
                                                ]
                                            }
                                        </option>
                                    );
                                },
                            )}
                        </select>
                    </label>
                    <input
                        type="submit"
                        className="button"
                        value="Submit"
                    />
                </form>
                <div className="well-wrapper">
                    <div className={`well hidden`} id="success-well">
                        Question successfully added!
                    </div>
                    <div className={`well hidden`} id="failure-well">
                        Unable to add question. Please try your
                        request again.
                    </div>
                </div>
            </div>
        );
    }
}

export default FormView;

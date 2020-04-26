import React, { useEffect, useState } from "react";
import axios from "axios";
import "../stylesheets/App.css";
import Question from "./Question";
import { Redirect } from "react-router";
import Search from "./Search";
import $ from "jquery";

const QuestionView = () => {
    const [state, setState] = useState({
        questions: [],
        page: localStorage.getItem("currentPage"),
        totalQuestions: 0,
        categories: {},
        currentCategory: null,
    });

    // Get questions only on mount and set up page number in LS
    useEffect(() => {
        if (!localStorage.getItem("currentPage")) {
            localStorage.setItem("currentPage", "1");
        }

        getQuestions();
    }, []);

    // Update questions whenever the page number changes via the pagination
    useEffect(() => {
        getQuestions();
    }, [state.page]);

    const getQuestions = () => {
        axios
            .get(`/questions?page=${state.page}`)
            .then(result => {
                console.log("Success: ", result);

                setState({
                    ...state,
                    questions: result.data.questions,
                    totalQuestions: result.data.total_questions,
                    categories: result.data.categories,
                    currentCategory: result.data.current_category,
                });
            })
            .catch(error => {
                console.log("Error: ", error);
                alert(
                    "Unable to load questions. Please try your request again",
                );
            });
    };

    const selectPage = num => {
        localStorage.setItem("currentPage", num);
        setState({ ...state, page: num });
    };

    const createPagination = () => {
        const pageNumbers = [];
        const maxPage = Math.ceil(state.totalQuestions / 10);

        for (let i = 1; i <= maxPage; i++) {
            pageNumbers.push(
                <span
                    key={i}
                    className={`page-num ${
                        i === state.page ? "active" : ""
                    }`}
                    onClick={() => {
                        selectPage(i);
                    }}>
                    {i}
                </span>,
            );
        }
        return pageNumbers;
    };

    const getByCategory = id => {
        $.ajax({
            url: `/categories/${id}/questions`,
            type: "GET",
            success: result => {
                setState({
                    ...state,
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category,
                });
            },
            error: error => {
                alert(
                    "Unable to load questions. Please try your request again",
                );
            },
        });
    };

    const submitSearch = searchTerm => {
        $.ajax({
            url: `/search`,
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            data: JSON.stringify({ searchTerm: searchTerm }),
            xhrFields: {
                withCredentials: true,
            },
            crossDomain: true,
            success: result => {
                setState({
                    ...state,
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category,
                });
            },
            error: error => {
                alert(
                    "Unable to load questions. Please try your request again",
                );
            },
        });
    };

    const questionAction = id => action => {
        if (action === "DELETE") {
            if (
                window.confirm(
                    "are you sure you want to delete the question?",
                )
            ) {
                $.ajax({
                    url: `/questions/${id}`,
                    type: "DELETE",
                    success: result => {
                        getQuestions();
                    },
                    error: error => {
                        alert(
                            "Unable to load questions. Please try your request again",
                        );
                    },
                });
            }
        }
    };

    return (
        <div className="question-view">
            <div className="categories-list">
                <h2 onClick={() => getQuestions()}>Categories</h2>
                {state.categories && (
                    <ul>
                        {Object.keys(state.categories).map(id => (
                            <li
                                key={id}
                                onClick={() => {
                                    getByCategory(id);
                                }}>
                                {state.categories[id]}
                                <img
                                    className="category"
                                    src={`${state.categories[id]}.svg`}
                                />
                            </li>
                        ))}
                    </ul>
                )}
                <Search submitSearch={submitSearch} />
            </div>
            <div className="questions-list">
                <h2>Questions</h2>
                {state.questions.map((q, ind) => (
                    <Question
                        key={q.id}
                        question={q.question}
                        answer={q.answer}
                        category={state.categories[q.category]}
                        difficulty={q.difficulty}
                        questionAction={questionAction(q.id)}
                    />
                ))}
                <div className="pagination-menu">
                    <Redirect to={`/questions?page=${state.page}`} />
                    {createPagination()}
                </div>
            </div>
        </div>
    );
};

export default QuestionView;

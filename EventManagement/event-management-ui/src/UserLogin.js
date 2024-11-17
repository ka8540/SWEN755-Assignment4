import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField, Tabs, Tab } from "@mui/material";
import { LOGIN_IMAGE_URL } from './constants';
import "./Login.css";

export default function UserLogin() {
    const navigate = useNavigate();
    const [currentTabIndex, setCurrentTabIndex] = useState(0);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [studentEmail, setStudentEmail] = useState("");
    const [major, setMajor] = useState("");
    const [error, setError] = useState("");

    const handleTabChange = (e, newValue) => {
        setCurrentTabIndex(newValue);
        setError("");
    };

    const handleLoginOnClick = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.message || "Invalid Credentials");
                throw new Error(data.message);
            }

            localStorage.setItem("token", data.access_token);

            navigate("/userdashboard");
        } catch (error) {
            setError(error.message);
        }
    };

    const handleRegisterOnClick = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    student_email: studentEmail,
                    username,
                    password,
                    major,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.message || "Registration Failed");
                throw new Error(data.message);
            }

            alert("Registration Successful! Please log in.");
            setCurrentTabIndex(0); 
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <div className="container">
            <div className="subContainer">
                <img src={LOGIN_IMAGE_URL} alt="login page" className="image" />
                <div className="typewriter-text">RIT</div>
            </div>
            <div className="tabContainer">
                <div className="title">GatherHub</div>
                <Tabs
                    value={currentTabIndex}
                    onChange={handleTabChange}
                    centered
                    sx={{
                        "& .MuiTabs-indicator": {
                            backgroundColor: "#ff7700", // Change the indicator line color
                        },
                    }}
                >
                    <Tab
                        label="Login"
                        sx={{
                            "&.Mui-selected": {
                                color: "#ff7700", // Change the selected tab color
                            },
                        }}
                    />
                    <Tab
                        label="Register"
                        sx={{
                            "&.Mui-selected": {
                                color: "#ff7700", // Change the selected tab color
                            },
                        }}
                    />
                </Tabs>
                {currentTabIndex === 0 && (
                    <div className="tab">
                        <TextField
                            label="Username"
                            variant="outlined"
                            size="small"
                            fullWidth
                            margin="normal"
                            required
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <TextField
                            label="Password"
                            variant="outlined"
                            size="small"
                            fullWidth
                            margin="normal"
                            required
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <Button
                            style={{ backgroundColor: "#ff7700", marginTop: "1rem" }}
                            variant="contained"
                            fullWidth
                            onClick={handleLoginOnClick}
                        >
                            LOGIN
                        </Button>
                        {error && (
                            <div style={{ color: "red", textAlign: "center", marginTop: "1rem" }}>
                                {error}
                            </div>
                        )}
                    </div>
                )}
                {currentTabIndex === 1 && (
                    <div className="tab">
                        <TextField
                            label="Student Email"
                            variant="outlined"
                            size="small"
                            fullWidth
                            margin="normal"
                            required
                            value={studentEmail}
                            onChange={(e) => setStudentEmail(e.target.value)}
                        />
                        <TextField
                            label="Username"
                            variant="outlined"
                            size="small"
                            fullWidth
                            margin="normal"
                            required
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                        <TextField
                            label="Password"
                            variant="outlined"
                            size="small"
                            fullWidth
                            margin="normal"
                            required
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                        <TextField
                            label="Major (UG or G)"
                            variant="outlined"
                            size="small"
                            fullWidth
                            margin="normal"
                            required
                            value={major}
                            onChange={(e) => setMajor(e.target.value)}
                        />
                        <Button
                            style={{ backgroundColor: "#ff7700", marginTop: "1rem" }}
                            variant="contained"
                            fullWidth
                            onClick={handleRegisterOnClick}
                        >
                            REGISTER
                        </Button>
                        {error && (
                            <div style={{ color: "red", textAlign: "center", marginTop: "1rem" }}>
                                {error}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

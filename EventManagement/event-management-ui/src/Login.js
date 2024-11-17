import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button, TextField, Tabs, Tab } from "@mui/material";
import { LOGIN_IMAGE_URL } from './constants';
import "./Login.css";

export default function Login() {
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLoginOnClick = async () => {
        try {
            const response = await fetch("http://127.0.0.1:5000/admin/login", {
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

            navigate("/admindashboard");
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <div className="container">
            <div className="subContainer">
            <img src={LOGIN_IMAGE_URL} alt="login page" className="image"/>
                <div className="typewriter-text">RIT</div>
               
            </div>
            <div className="tabContainer">
            <div className="title">GatherHub</div>
                <Tabs
                    value={0}
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
                </Tabs>
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
            </div>
        </div>
    );
}

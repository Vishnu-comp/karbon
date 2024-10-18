


import React, { useState } from 'react';
import axios from 'axios';
import { FaFileUpload, FaCheckCircle, FaExclamationTriangle, FaExclamationCircle, FaRegQuestionCircle } from 'react-icons/fa';

function App() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [result, setResult] = useState(null);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false); // Loading state

    // Handle file upload
    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setError("");
    };

    // Handle form submission
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!selectedFile) {
            setError("Please upload a file");
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);
        setLoading(true); // Set loading state

        try {
            const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            setResult(response.data);
        } catch (err) {
            setError("Failed to upload file or process data.");
            console.error(err);
        } finally {
            setLoading(false); // Reset loading state
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-100 p-4">
            <div className="bg-white shadow-md rounded-lg p-6 w-full max-w-md">
                <h2 className="text-2xl font-bold mb-4 text-center">Upload data.json File</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="file"
                        onChange={handleFileChange}
                        accept=".json"
                        className="block w-full text-sm text-gray-500
                                   file:mr-4 file:py-2 file:px-4
                                   file:rounded-md file:border-0
                                   file:text-sm file:font-semibold
                                   file:bg-gray-50 file:text-gray-700
                                   hover:file:bg-gray-100"
                    />
                    <button
                        type="submit"
                        className="mt-4 w-full py-2 px-4 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 transition duration-200"
                    >
                        {loading ? "Uploading..." : "Submit"}
                    </button>
                </form>

                {error && <p className="mt-4 text-red-500">{error}</p>}

                {result && (
                    <div className="mt-6 bg-white shadow-lg rounded-lg p-4 border border-gray-300">
                        <h3 className="text-lg font-semibold">Results:</h3>
                        <ul className="mt-2 space-y-3">
                            {Object.entries(result.flags).map(([flagName, flagValue]) => {
                                let flagColor;
                                let flagText;
                                let IconComponent;

                                // Determine color and text based on flag value
                                switch (flagValue) {
                                    case 0:
                                        flagColor = 'bg-red-100 text-red-800'; // RED
                                        flagText = 'Critical Risk';
                                        IconComponent = FaExclamationCircle;
                                        break;
                                    case 1:
                                        flagColor = 'bg-green-100 text-green-800'; // GREEN
                                        flagText = 'Low Risk';
                                        IconComponent = FaCheckCircle;
                                        break;
                                    case 2:
                                        flagColor = 'bg-yellow-100 text-yellow-800'; // AMBER
                                        flagText = 'Medium Risk';
                                        IconComponent = FaExclamationTriangle;
                                        break;
                                    case 3:
                                        flagColor = 'bg-yellow-200 text-yellow-900'; // MEDIUM_RISK
                                        flagText = 'Medium Risk (Display Purpose)';
                                        IconComponent = FaExclamationTriangle;
                                        break;
                                    case 4:
                                        flagColor = 'bg-gray-100 text-gray-800'; // WHITE
                                        flagText = 'Data Missing';
                                        IconComponent = FaRegQuestionCircle;
                                        break;
                                    default:
                                        flagColor = 'bg-gray-100 text-gray-800'; // Default
                                        flagText = 'Unknown';
                                }

                                return (
                                    <li key={flagName} className={`flex items-center p-3 rounded-md ${flagColor} transition duration-200 hover:shadow-lg`}>
                                        <span className="mr-2">
                                            {IconComponent && <IconComponent className="h-5 w-5" />}
                                        </span>
                                        <span className="font-medium">{flagName.replace(/_/g, ' ')}</span>
                                        <span className="ml-auto">{flagText}</span>
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;


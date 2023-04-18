import React from 'react';
import URLAdd from './URLAdd';
import { BASE_URL } from "@/config/constants";

const URLAdder = () => {
  async function handleSubmit(url: string) {
    console.log(url);
    await fetch(BASE_URL+ "/addWebpage", {
      method: "POST",
      mode: "cors",
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        URL: url
      })
    })
  };

  return (
    <div>
      <URLAdd onSubmit={handleSubmit} />
    </div>
  );
}

export default URLAdder;

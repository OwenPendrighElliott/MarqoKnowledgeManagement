import React from "react";
import DocumentAdd from "./DocumentAdd";
import { BASE_URL } from "@/config/constants";

const KnowledgeAdder: React.FC = () => {
  async function handleSubmit(text: string) {
    // Send the text to your API here
    console.log(text);
    await fetch(BASE_URL+ "/addKnowledge", {
      method: "POST",
      mode: "cors",
      body: JSON.stringify({
        document: text
      })
    })
  };

  return <DocumentAdd onSubmit={handleSubmit} />;
};

export default KnowledgeAdder;

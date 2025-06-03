import React from "react";
import FeedCard from "./FeedCard";

const dummyPosts = [
  {
    post_id: "1",
    post_title: "How to Grow Organic Tomatoes",
    post_content:
      "Growing organic tomatoes requires proper compost, timely watering, and good sunlight. Using natural fertilizers like cow dung and neem spray helps keep pests away while ensuring healthy growth. You can also plant basil nearby to naturally repel insects and improve tomato flavor.",
    author: "Ramesh Shrestha",
  },
  {
    post_id: "2",
    post_title: "पानीको सही व्यवस्थापन",
    post_content:
      "खेतीमा पानी व्यवस्थापन अत्यन्त महत्वपूर्ण छ। ड्रिप इरिगेसन, मल्चिंग र वर्षा पानी संकलन प्रणालीलाई उपयोग गर्दा खेती स्याउला हुन्छ र उत्पादन पनि बढ्छ। कृषकहरूले अब सस्तो प्रविधिहरू अपनाएर सिँचाइ समस्या समाधान गर्न सक्छन्।",
    author: "Sita Gurung",
  },
  {
    post_id: "3",
    post_title: "Using Compost for Better Soil",
    post_content:
      "Composting is an eco-friendly method to enrich soil. Combine kitchen waste, dry leaves, and cow dung in a pit for 3-4 weeks. The resulting compost boosts nutrients in the soil naturally. It also improves moisture retention and reduces dependence on chemical fertilizers.",
    author: "Anil Basnet",
  },
  {
    post_id: "4",
    post_title: "Best Practices for Rice Farming",
    post_content:
      "Rice farming thrives in well-irrigated fields with seasonal rainfall. Plowing the land thoroughly, choosing high-yield seed varieties, and applying timely organic manure can increase rice yield significantly. Maintain proper spacing between plants to prevent fungal diseases.",
    author: "Manju Poudel",
  },
];

const Feed = () => {
  return (
    <div className="flex justify-center px-4 py-10 bg-[#fdfde3] min-h-screen">
      <div className="grid gap-8 max-w-4xl w-full">
        {dummyPosts.map((post) => (
          <FeedCard
            key={post.post_id}
            title={post.post_title}
            content={post.post_content}
            author={post.author}
          />
        ))}
      </div>
    </div>
  );
};

export default Feed;

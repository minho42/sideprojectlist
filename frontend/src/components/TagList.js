const TagList = ({ data, selectedTag, setSelectedTag }) => {
  const uniqueTags = [{ name: "all", count: data.length }];
  const setUniqueTags = () => {
    data.filter((project) => {
      return project.tags.filter((tag) => {
        if (uniqueTags.some((t) => t.name.toLowerCase() === tag.toLowerCase())) {
          return uniqueTags.forEach((o) => {
            if (o.name.toLowerCase() === tag.toLowerCase()) {
              return (o.count += 1);
            }
          });
        } else {
          return uniqueTags.push({ name: tag, count: 1 });
        }
      });
    });
  };

  const sortUniqueTags = () => {
    uniqueTags.sort((a, b) => {
      return a.count < b.count ? 1 : a.count > b.count ? -1 : a.name > b.name ? 1 : a.name < b.name ? -1 : 0;
    });
  };

  setUniqueTags();
  sortUniqueTags();

  const handleTagSelect = (e) => {
    setSelectedTag(e.currentTarget.getAttribute("value"));
  };

  return (
    <div className="flex items-center flex-wrap mb-6">
      {uniqueTags.map((tag) => {
        return (
          <div
            key={tag.name}
            value={tag.name}
            onClick={handleTagSelect}
            className={`flex items-center cursor-pointer rounded-xl font-medium text-sm px-2 py-1 mr-1 mt-1 
            ${
              tag.name === selectedTag ? "bg-purple-300 hover:bg-purple-400" : "bg-gray-200 hover:bg-gray-300"
            }
          `}
          >
            <div>{tag.name}</div>
            <div className="rounded-full bg-white text-xs px-1 ml-1 font-normal">{tag.count}</div>
          </div>
        );
      })}
    </div>
  );
};

export default TagList;

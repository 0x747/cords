function showLikesModal(id) {
    document.getElementById(id).showModal()
}

function closeLikesModal(id) {
    document.getElementById(id).close()
}

function showComments(id, element) {
    commentBox = document.getElementById(id);

    if (commentBox.style.display == "none" || !commentBox.style.display) {
        commentBox.style.display = "block";
        element.innerHTML = element.innerHTML.replace("View", "Hide");
        element.style.boxShadow = "2px 0px 5px var(--light-button-hover)";
        element.style.borderRadius = "0px";
    } else {
        commentBox.style.display = "none";
        element.innerHTML = element.innerHTML.replace("Hide", "View");
        element.style.borderBottomLeftRadius = "5px";
        element.style.borderBottomRightRadius = "5px";
    }
}

function snowflakeIdToDate(snowflakeId, id) {
    // Define constants
    console.log("hi");
    const EPOCH = 1288834974657;
    const SEQUENCE_BITS = 12;
    const WORKER_BITS = 5;
    const DATA_CENTER_BITS = 5;

    const WORKER_SHIFT = SEQUENCE_BITS;
    const DATA_CENTER_SHIFT = SEQUENCE_BITS + WORKER_BITS;
    const TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_BITS + DATA_CENTER_BITS;

    // Extract timestamp from Snowflake ID
    const timestamp = (snowflakeId >> TIMESTAMP_SHIFT) + EPOCH;

    // Convert timestamp to date
    const date = new Date(timestamp);

    // Format the date
    const formattedDate = date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
    });

    document.getElementById(id).innerHTML = formattedDate;
}


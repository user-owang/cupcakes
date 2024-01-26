function appendCupcake(cake) {
  $(".cupcake-list").append(
    `<li><a href="/${cake["id"]}">${cake["flavor"]}</a></li>`
  );
}

async function listCupcakes() {
  const res = await axios.get("/api/cupcakes");
  for (let cake of res.data["cupcakes"]) {
    appendCupcake(cake);
  }
}

async function submitHandler(evt) {
  evt.preventDefault();
  const flavor = $("#flavor").val();
  const size = $("#size").val();
  const rating = $("#rating").val();
  let image = $("#image").val();

  if (image === "") {
    image = null;
  }

  const res = await axios.post("/api/cupcakes", {
    flavor: flavor,
    size: size,
    rating: rating,
    image: image,
  });

  appendCupcake(res.data["cupcake"]);
}

listCupcakes();
$(".new-cupcake").submit(submitHandler);

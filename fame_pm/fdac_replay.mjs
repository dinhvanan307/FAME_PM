// Run the unchanged upstream client on the examples included in its OpenAPI release.
// The transport is local. These responses and IDs are fixtures, not pilot activity.
import assert from "node:assert/strict";
import {readFile} from "node:fs/promises";
import {pathToFileURL} from "node:url";

const [clientPath, specPath] = process.argv.slice(2);
const {IoTCatalogueService} = await import(pathToFileURL(clientPath));
const spec = JSON.parse(await readFile(specPath, "utf8"));
const examples = spec.paths["/searchAssets"].post.requestBody.content["application/json"].examples;
const assetIds = ["fixture-asset"];
const client = new IoTCatalogueService({baseURL: "https://fixture.invalid", token: "fixture"});
const passed = [];
for (const [name, example] of Object.entries(examples)) {
  const calls = [];
  const answer = {results: [{id: assetIds[0]}]};
  globalThis.fetch = async (url, options) => {
    assert.equal(new URL(url).origin, "https://fixture.invalid");
    assert.equal(options.method, "POST");
    const path = new URL(url).pathname;
    calls.push(path);
    const body = JSON.parse(options.body);
    if (path === "/api/workspaces/generateTemporaryWorkspace") {
      assert.deepEqual(body.data.components.ids, assetIds);
      return Response.json({token: "fixture-workspace"});
    }
    assert.equal(path, "/api/data/search");
    assert.deepEqual(body, example.value);
    return Response.json(answer);
  };
  const result = await client.searchAssets(assetIds, example.value);
  assert.deepEqual(calls, ["/api/workspaces/generateTemporaryWorkspace", "/api/data/search"]);
  assert.deepEqual(result, answer);
  passed.push(name);
}
assert.ok(passed.length > 0);
console.log(JSON.stringify({method: "IoTCatalogueService.searchAssets", examples: passed,
                            transport: "in-memory fetch fixture", network_requests: 0}));

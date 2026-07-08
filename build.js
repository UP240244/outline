/* oxlint-disable no-console */
/* oxlint-disable @typescript-oxlint/no-var-requires */
/* oxlint-disable no-undef */
const { exec } = require("child_process");
const { readdirSync, existsSync, mkdirSync, copyFileSync } = require("fs");

const getDirectories = (source) =>
  readdirSync(source, { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);

/**
 * Executes a shell command and return it as a Promise.
 * @param cmd {string}
 * @return {Promise<string>}
 */
function execAsync(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        resolve(stdout ? stdout : stderr);
      }
    });
  });
}

async function build() {
  // Clean previous build
  console.log("Clean previous build…");

  await Promise.all([
    execAsync("rm -rf ./build/server"),
    execAsync("rm -rf ./build/plugins"),
  ]);

  const d = getDirectories("./plugins");

  // Compile server and shared
  console.log("Compiling…");
  const swc = (src, out) =>
    execAsync(
      `yarn swc "${src}" -d "${out}" --strip-leading-paths --extensions .ts,.tsx --ignore "**/*.test.ts,**/*.test.tsx,**/__mocks__/**" --quiet`
    );

  await Promise.all([
    swc("./server", "./build/server"),
    swc("./shared", "./build/shared"),
  ]);

  // SWC's --strip-leading-paths removes only the topmost path segment, so a
  // `plugins/<name>/server` input keeps `<name>/server/…` and lands correctly
  // under a `./build/plugins` output directory.
  for (const plugin of d) {
    const hasServer = existsSync(`./plugins/${plugin}/server`);

    if (hasServer) {
      await swc(`./plugins/${plugin}/server`, "./build/plugins");
    }

    const hasShared = existsSync(`./plugins/${plugin}/shared`);

    if (hasShared) {
      await swc(`./plugins/${plugin}/shared`, "./build/plugins");
    }
  }

  // Copy static files
  console.log("Copying static files…");
  await Promise.all([
    execAsync(
      "cp ./server/collaboration/Procfile ./build/server/collaboration/Procfile"
    ),
    execAsync(
      "cp ./server/static/error.dev.html ./build/server/error.dev.html"
    ),
    execAsync(
      "cp ./server/static/error.prod.html ./build/server/error.prod.html"
    ),
    copyFileSync("./package.json", "./build/package.json"),

    ...d.map(async (plugin) => {
      mkdirSync(`./build/plugins/${plugin}`, { recursive: true });
      const sourcePath = `./plugins/${plugin}/plugin.json`;
      if (existsSync(sourcePath)) {
        copyFileSync(sourcePath, `./build/plugins/${plugin}/plugin.json`);
      } else {
        console.log(`[Aviso] El plugin "${plugin}" no contiene plugin.json, saltando...`);
      }
    }),
  ]);

  console.log("Done!");
}

void build();

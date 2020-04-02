const dotenv = require('dotenv')
const contentfulImport = require('contentful-import')

var argv = require('minimist')(process.argv.slice(2))

dotenv.load()

const spaceId = process.env.CONTENTFUL_SPACE_ID
const managementToken = process.env.CONTENTFUL_MANAGEMENT_TOKEN
const environmentId = process.env.CONTENTFUL_ENV || 'master'

if (!spaceId) {
  console.error('set CONTENTFUL_SPACE_ID is required')
}

if (!managementToken) {
  console.error('set CONTENTFUL_MANAGEMENT_TOKEN is required')
}

const options = {
  spaceId,
  managementToken,
  environmentId,
  contentModelOnly: true,
  contentFile: argv.file || 'contentful.json'
}

contentfulImport(options)

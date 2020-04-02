const path = require('path')
const templater = require('json-templater/object')
const dotenv = require('dotenv')
const contentfulImport = require('contentful-import')
const contentful = require('contentful-management')

dotenv.load()

const spaceId = process.env.CONTENTFUL_SPACE_ID
const managementToken = process.env.CONTENTFUL_MANAGEMENT_TOKEN
const env = process.env.CONTENTFUL_ENV

if (!spaceId) {
  console.error('set CONTENTFUL_SPACE_ID is required')
  process.exit(1)
}

if (!managementToken) {
  console.error('set CONTENTFUL_MANAGEMENT_TOKEN is required')
  process.exit(1)
}

if (!env) {
  console.error('set CONTENTFUL_ENV is required')
  process.exit(1)
}

const client = contentful.createClient({
  accessToken: managementToken
})

const importWebhooks = async () => {
  const space = await client.getSpace(spaceId)
  const oldWebhooks = await space.getWebhooks()

  try {
    const promises = oldWebhooks.items.map(async ({ sys: { id } }) => {
      const webhook = await space.getWebhook(id)
      if (webhook.name.trim().endsWith(env)) {
        return webhook.delete()
      }

      return Promise.resolve()
    })

    await Promise.all(promises)

    let { webhooks } = require(path.join(__dirname, 'webhooks.json'))

    webhooks = templater(webhooks, { ...process.env })

    const options = {
      spaceId,
      managementToken,
      skipContentModel: true,
      content: {
        webhooks
      }
    }

    await contentfulImport(options)
  } catch (error) {
    console.error(error)

    console.log('[ERROR] Importing webhooks. Rolling back changes')
    await contentfulImport({
      spaceId,
      managementToken,
      skipContentModel: true,
      content: {
        webhooks: oldWebhooks.items
      }
    })
  }
}

importWebhooks()

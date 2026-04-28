# SKILL.md - shopify_admin

## Name
shopify_admin

## Description
Full Shopify Admin API integration via GraphQL for GrowBiz Media stores. Enables automated product management, order analysis, inventory monitoring, and content generation across DoodleType and other Shopify stores.

## When to Use
- Managing Shopify products programmatically
- Analyzing sales data and trends
- Monitoring inventory levels and low-stock alerts
- Generating product descriptions and SEO content
- Detecting inventory risks across stores
- Processing order data for reporting

## Inputs
| Name | Type | Required | Description |
|------|------|----------|-------------|
| action | enum | yes | get_products, get_orders, analyze_sales, detect_inventory_risk, generate_product_content, update_product, create_product |
| store_domain | string | yes | Shopify store domain (e.g., doodletype.myshopify.com) |
| access_token | string | yes | Shopify Admin API access token |
| params | object | no | Action-specific parameters |

## Outputs
GraphQL response data formatted per action type

## Authentication
OAuth2 with Shopify Admin API:
- Required scopes: read_products, write_products, read_orders, read_customers, read_inventory
- Token storage: secure credentials store
- Refresh: automatic on expiry

## Rate Limiting
Shopify GraphQL rate limits enforced:
- Cost-based throttling (50 points/second)
- Automatic retry with exponential backoff
- Request cost tracking

## Logic
- GraphQL wrapper with error handling
- Multi-store support via store_domain param
- Webhook event processing for real-time updates
- Agent attribution for audit trail

## Access Control
- **RodZilla:** All actions (owner, technical implementation)
- **Frank:** Read access, coordination
- **FrankCMO:** get_products, analyze_sales, generate_product_content
- **FrankCFO:** analyze_sales, get_orders

## Owner
RodZilla (Engineering/Technical Team)

## Triggers
- "shopify"
- "products"
- "orders"
- "inventory"
- "sales analysis"

## Permissions
- shopify_api_read
- shopify_api_write
- memory_read
- memory_write

## Preferred Model
deepseek-chat

## Transport
GraphQL over HTTPS with webhook listeners

<!DOCTYPE html>
<html>
<head>
	<title>Shopify Inventory Sync Script</title>
</head>
<body>
	<h1>Shopify Inventory Sync Script</h1>
	<p>This Python script uses the Shopify REST API to sync the inventory levels of multiple Shopify stores. It can be used to ensure that the inventory levels for the same products are consistent across all stores.</p>
	<h2>Getting Started</h2>
	<ol>
		<li>Clone this repository to your local machine.</li>
		<li>Install the required Python packages by running <code>pip install -r requirements.txt</code>.</li>
		<li>Create a <code>stores.ini</code> file in the root directory of the project with the API credentials and URLs for each store that you want to sync inventory levels for. The <code>stores.ini</code> file should have a section for each store with the keys <code>api_key</code>, <code>password</code>, and <code>url</code>. Here's an example <code>stores.ini</code> file:</li>
	</ol>
	<pre><code>[Store A]
api_key = your_api_key
password = your_api_password
url = https://store-a.myshopify.com
[Store B]
api_key = your_api_key
password = your_api_password
url = https://store-b.myshopify.com

[Store C]
api_key = your_api_key
password = your_api_password
url = https://store-c.myshopify.com
</code></pre>
<ol start="4">
<li>Replace the <code>location_id</code> variable in the script with the appropriate location ID for each store.</li>
<li>Run the script using the command <code>python sync_inventory.py</code>.</li>
</ol>
<h2>Contributing</h2>
<p>Contributions are welcome! If you have any suggestions or improvements for this script, feel free to open an issue or submit a pull request.</p>
<h2>License</h2>
<p>This script is licensed under the MIT License. See the <code>LICENSE</code> file for details.</p>
<h2>Acknowledgements</h2>
<p>This script was created using the Shopify REST API and the Python <code>requests</code> library. Special thanks to the Shopify API documentation for providing helpful resources and examples.</p>

</body>
</html>

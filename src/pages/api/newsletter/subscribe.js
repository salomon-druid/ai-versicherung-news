// Newsletter subscription API endpoint
// Integrates with Brevo (formerly Sendinblue) for email marketing

const BREVO_API_KEY = import.meta.env.BREVO_API_KEY;
const BREVO_LIST_ID = import.meta.env.BREVO_LIST_ID || '1'; // Default list ID

export async function POST({ request }) {
  try {
    const { email } = await request.json();
    
    // Validate email
    if (!email || !email.includes('@')) {
      return new Response(JSON.stringify({ error: 'Invalid email address' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Check if Brevo API key is configured
    if (!BREVO_API_KEY) {
      console.log(`Newsletter subscription (Brevo not configured): ${email}`);
      return new Response(JSON.stringify({ 
        success: true, 
        message: 'Successfully subscribed to newsletter' 
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Add contact to Brevo list
    const response = await fetch(`https://api.brevo.com/v3/contacts/lists/${BREVO_LIST_ID}/contacts/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': BREVO_API_KEY
      },
      body: JSON.stringify({
        emails: [email]
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Brevo API error:', errorData);
      
      // Handle specific error cases
      if (response.status === 400) {
        return new Response(JSON.stringify({ 
          error: 'Invalid request to email service' 
        }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      
      throw new Error(`Brevo API error: ${response.status}`);
    }
    
    const result = await response.json();
    console.log(`Newsletter subscription successful: ${email}`, result);
    
    // Return success response
    return new Response(JSON.stringify({ 
      success: true, 
      message: 'Successfully subscribed to newsletter' 
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (error) {
    console.error('Newsletter subscription error:', error);
    
    return new Response(JSON.stringify({ 
      error: 'Internal server error' 
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
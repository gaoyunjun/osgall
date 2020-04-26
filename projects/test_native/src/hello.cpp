
#include "myNativeApp.h"

#include <osg/MatrixTransform>

//ʵ��ִ�е�APP����
class myAPP
    :public myNativeApp
{
public:

    myAPP(){}
    virtual ~myAPP(){}
    
    osg::ref_ptr<osg::MatrixTransform> mt;

    //GL��ʼ�� ��Ϣ
    virtual void onGLCreate( int x,int y,int width,int height )
    {
    
    }
    
    //GL���� ��Ϣ
    virtual void onGLDistroy()
    {
        
    }
    
    //GL���� ��Ϣ
    virtual void onGLDraw()
    {
#if 1
        // Just fill the screen with a color.
        glClearColor(
            ((float)this->state.x)/this->width
            , this->state.angle
            ,((float)this->state.y)/this->height
            , 1);
        glClear(GL_COLOR_BUFFER_BIT);
#endif
        
    }
    
};


/**
 * This is the main entry point of a native application that is using
 * android_native_app_glue.  It runs in its own thread, with its own
 * event loop for receiving input events and doing other things.
 */
void android_main(struct android_app* state) 
{
    // Make sure glue isn't stripped.
    app_dummy();
    
    //����APP����
    myAPP engine;
    engine.Create(state);
    
    //����
    engine.run();
}
//END_INCLUDE(all)